/**
 * GAP-003 Query Control API - Resume Endpoint
 *
 * File: app/api/query-control/queries/[queryId]/resume/route.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: REST API for resuming paused queries from checkpoints
 *
 * Endpoint:
 * - POST /api/query-control/queries/[queryId]/resume - Resume query from checkpoint
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
 * POST /api/query-control/queries/[queryId]/resume
 * Resume a paused query from latest checkpoint
 *
 * Query Parameters:
 * - checkpointId?: string - Specific checkpoint to resume from (optional, defaults to latest)
 *
 * Returns:
 * {
 *   success: boolean,
 *   resumedFrom?: string,
 *   state: QueryState,
 *   resumeTimeMs: number,
 *   checkpoint?: Checkpoint
 * }
 */
export async function POST(
  request: NextRequest,
  { params }: { params: { queryId: string } }
) {
  try {
    const { queryId } = params;
    const searchParams = request.nextUrl.searchParams;
    const checkpointId = searchParams.get('checkpointId') || undefined;

    const service = getService();
    const result = service.resumeQuery(queryId, checkpointId);

    if (!result.success) {
      return NextResponse.json(
        {
          error: 'Failed to resume query',
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
      resumedFrom: result.resumedFrom,
      state: result.state,
      resumeTimeMs: result.resumeTimeMs,
      checkpoint: result.checkpoint ? {
        id: result.checkpoint.id,
        queryId: result.checkpoint.queryId,
        state: result.checkpoint.state,
        timestamp: result.checkpoint.timestamp
      } : undefined,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error(`Error resuming query ${params.queryId}:`, error);
    return NextResponse.json(
      {
        error: 'Failed to resume query',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
