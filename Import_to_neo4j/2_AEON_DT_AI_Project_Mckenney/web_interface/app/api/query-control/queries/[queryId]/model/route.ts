/**
 * GAP-003 Query Control API - Model Switcher Endpoint
 *
 * File: app/api/query-control/queries/[queryId]/model/route.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: REST API for model hot-swapping during query execution
 *
 * Endpoint:
 * - POST /api/query-control/queries/[queryId]/model - Switch AI model
 */

import { NextRequest, NextResponse } from 'next/server';
import { QueryControlService } from '@/lib/query-control/query-control-service';
import { ModelType } from '@/lib/query-control/model/model-switcher';

// Singleton service instance
let serviceInstance: QueryControlService | null = null;

function getService(): QueryControlService {
  if (!serviceInstance) {
    serviceInstance = new QueryControlService();
  }
  return serviceInstance;
}

/**
 * POST /api/query-control/queries/[queryId]/model
 * Hot-swap AI model for query
 *
 * Body:
 * {
 *   model: "sonnet" | "opus" | "haiku"
 * }
 *
 * Returns:
 * {
 *   success: boolean,
 *   previousModel: ModelType,
 *   newModel: ModelType,
 *   switchTimeMs: number
 * }
 */
export async function POST(
  request: NextRequest,
  { params }: { params: { queryId: string } }
) {
  try {
    const { queryId } = params;
    const body = await request.json();

    // Validate model parameter
    const validModels: ModelType[] = ['sonnet', 'opus', 'haiku'];
    if (!body.model || !validModels.includes(body.model)) {
      return NextResponse.json(
        {
          error: 'Invalid model parameter',
          message: `Model must be one of: ${validModels.join(', ')}`,
          received: body.model
        },
        { status: 400 }
      );
    }

    const service = getService();
    const result = service.switchModel(queryId, body.model);

    if (!result.success) {
      return NextResponse.json(
        {
          error: 'Failed to switch model',
          queryId,
          message: result.error,
          previousModel: result.previousModel,
          requestedModel: body.model
        },
        { status: 400 }
      );
    }

    return NextResponse.json({
      success: true,
      queryId,
      previousModel: result.previousModel,
      newModel: result.newModel,
      switchTimeMs: result.switchTimeMs,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error(`Error switching model for query ${params.queryId}:`, error);
    return NextResponse.json(
      {
        error: 'Failed to switch model',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
