/**
 * GAP-003 Query Control API - Permissions Endpoint
 *
 * File: app/api/query-control/queries/[queryId]/permissions/route.ts
 * Created: 2025-11-15
 * Version: v1.0.0
 * Purpose: REST API for permission mode switching during query execution
 *
 * Endpoint:
 * - POST /api/query-control/queries/[queryId]/permissions - Switch permission mode
 */

import { NextRequest, NextResponse } from 'next/server';
import { QueryControlService } from '@/lib/query-control/query-control-service';
import { PermissionMode } from '@/lib/query-control/permissions/permission-manager';

// Singleton service instance
let serviceInstance: QueryControlService | null = null;

function getService(): QueryControlService {
  if (!serviceInstance) {
    serviceInstance = new QueryControlService();
  }
  return serviceInstance;
}

/**
 * POST /api/query-control/queries/[queryId]/permissions
 * Switch permission mode for query
 *
 * Body:
 * {
 *   permissionMode: "default" | "acceptEdits" | "bypassPermissions" | "plan"
 * }
 *
 * Returns:
 * {
 *   success: boolean,
 *   previousMode: PermissionMode,
 *   newMode: PermissionMode,
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

    // Validate permission mode parameter
    const validModes: PermissionMode[] = ['default', 'acceptEdits', 'bypassPermissions', 'plan'];
    if (!body.permissionMode || !validModes.includes(body.permissionMode)) {
      return NextResponse.json(
        {
          error: 'Invalid permissionMode parameter',
          message: `Permission mode must be one of: ${validModes.join(', ')}`,
          received: body.permissionMode
        },
        { status: 400 }
      );
    }

    const service = getService();
    const result = service.switchPermissionMode(queryId, body.permissionMode);

    if (!result.success) {
      return NextResponse.json(
        {
          error: 'Failed to switch permission mode',
          queryId,
          message: result.error,
          previousMode: result.previousMode,
          requestedMode: body.permissionMode
        },
        { status: 400 }
      );
    }

    return NextResponse.json({
      success: true,
      queryId,
      previousMode: result.previousMode,
      newMode: result.newMode,
      switchTimeMs: result.switchTimeMs,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error(`Error switching permission mode for query ${params.queryId}:`, error);
    return NextResponse.json(
      {
        error: 'Failed to switch permission mode',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
