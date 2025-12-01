/**
 * GAP-003 Query Control API - Query Details Endpoint
 *
 * File: app/api/query-control/queries/[queryId]/route.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: REST API for individual query operations
 *
 * Endpoints:
 * - GET /api/query-control/queries/[queryId] - Get query details
 * - DELETE /api/query-control/queries/[queryId] - Terminate query
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
 * GET /api/query-control/queries/[queryId]
 * Get query details including state, model, checkpoints
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { queryId: string } }
) {
  try {
    const { queryId } = params;
    const service = getService();

    // Get all queries and find the requested one
    const result = service.listQueries();
    const query = result.queries.find(q => q.queryId === queryId);

    if (!query) {
      return NextResponse.json(
        { error: 'Query not found', queryId },
        { status: 404 }
      );
    }

    return NextResponse.json({
      query,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error(`Error getting query ${params.queryId}:`, error);
    return NextResponse.json(
      {
        error: 'Failed to get query details',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

/**
 * DELETE /api/query-control/queries/[queryId]
 * Terminate a query
 */
export async function DELETE(
  request: NextRequest,
  { params }: { params: { queryId: string } }
) {
  try {
    const { queryId } = params;
    const service = getService();

    const result = service.terminateQuery(queryId);

    if (!result.success) {
      return NextResponse.json(
        {
          error: 'Failed to terminate query',
          queryId,
          message: result.error
        },
        { status: 400 }
      );
    }

    return NextResponse.json({
      success: true,
      queryId,
      finalState: result.finalState,
      terminateTimeMs: result.terminateTimeMs,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error(`Error terminating query ${params.queryId}:`, error);
    return NextResponse.json(
      {
        error: 'Failed to terminate query',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
