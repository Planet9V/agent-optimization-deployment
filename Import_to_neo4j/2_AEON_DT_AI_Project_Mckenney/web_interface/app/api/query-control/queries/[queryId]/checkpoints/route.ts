/**
 * GAP-003 Query Control API - Checkpoints Endpoint
 *
 * File: app/api/query-control/queries/[queryId]/checkpoints/route.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: REST API for listing and accessing query checkpoints
 *
 * Endpoint:
 * - GET /api/query-control/queries/[queryId]/checkpoints - List query checkpoints
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
 * GET /api/query-control/queries/[queryId]/checkpoints
 * List all checkpoints for a query
 *
 * Query Parameters:
 * - limit?: number - Max results (default: 50)
 * - offset?: number - Pagination offset (default: 0)
 *
 * Returns:
 * {
 *   queryId: string,
 *   checkpoints: Checkpoint[],
 *   total: number,
 *   latest?: Checkpoint
 * }
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { queryId: string } }
) {
  try {
    const { queryId } = params;
    const searchParams = request.nextUrl.searchParams;

    // Parse query parameters
    const limit = parseInt(searchParams.get('limit') || '50');
    const offset = parseInt(searchParams.get('offset') || '0');

    const service = getService();
    const checkpoints = service.getCheckpoints(queryId);

    // Sort by timestamp descending (newest first)
    const sortedCheckpoints = [...checkpoints].sort((a, b) => b.timestamp - a.timestamp);

    // Apply pagination
    const paginatedCheckpoints = sortedCheckpoints.slice(offset, offset + limit);

    // Format checkpoints for API response (omit full execution context for brevity)
    const formattedCheckpoints = paginatedCheckpoints.map(cp => ({
      id: cp.id,
      queryId: cp.queryId,
      state: cp.state,
      timestamp: cp.timestamp,
      timestampISO: new Date(cp.timestamp).toISOString(),
      model: cp.modelConfig.model,
      permissionMode: cp.permissionMode,
      hasExecutionContext: !!cp.executionContext
    }));

    return NextResponse.json({
      queryId,
      checkpoints: formattedCheckpoints,
      total: sortedCheckpoints.length,
      latest: sortedCheckpoints.length > 0 ? formattedCheckpoints[0] : undefined,
      pagination: {
        limit,
        offset,
        hasMore: offset + limit < sortedCheckpoints.length
      }
    });
  } catch (error) {
    console.error(`Error getting checkpoints for query ${params.queryId}:`, error);
    return NextResponse.json(
      {
        error: 'Failed to get checkpoints',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
