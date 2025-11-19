/**
 * GAP-003 Query Control API - Pause Endpoint
 *
 * File: app/api/query-control/queries/[queryId]/pause/route.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: REST API for pausing queries with checkpoint creation
 *
 * Endpoint:
 * - POST /api/query-control/queries/[queryId]/pause - Pause query and create checkpoint
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
 * POST /api/query-control/queries/[queryId]/pause
 * Pause a running query and create checkpoint
 *
 * Returns:
 * {
 *   success: boolean,
 *   checkpointId?: string,
 *   state: QueryState,
 *   pauseTimeMs: number
 * }
 */
export async function POST(
  request: NextRequest,
  { params }: { params: { queryId: string } }
) {
  try {
    const { queryId } = params;
    const service = getService();

    const result = service.pauseQuery(queryId);

    if (!result.success) {
      return NextResponse.json(
        {
          error: 'Failed to pause query',
          queryId,
          message: result.error,
          currentState: result.state
        },
        { status: 400 }
      );
    }

    return NextResponse.json({
      success: true,
      queryId,
      checkpointId: result.checkpointId,
      state: result.state,
      pauseTimeMs: result.pauseTimeMs,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error(`Error pausing query ${params.queryId}:`, error);
    return NextResponse.json(
      {
        error: 'Failed to pause query',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
