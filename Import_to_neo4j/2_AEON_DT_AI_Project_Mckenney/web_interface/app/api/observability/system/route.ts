/**
 * System Observability API Endpoint
 *
 * Returns real-time system metrics from observability modules
 */

import { NextRequest, NextResponse } from 'next/server';
import { observability } from '@/lib/observability';

export async function GET(request: NextRequest) {
  try {
    // Get real system health summary from observability manager
    const healthSummary = await observability.getHealthSummary();

    // Get real process metrics
    const memUsage = process.memoryUsage();
    const cpuUsage = process.cpuUsage();
    const uptime = process.uptime();

    // Calculate memory percentage
    const memoryPercentage = (memUsage.heapUsed / memUsage.heapTotal) * 100;

    // Determine status based on real metrics
    let status: 'healthy' | 'warning' | 'critical' = 'healthy';
    if (memoryPercentage > 90) {
      status = 'critical';
    } else if (memoryPercentage > 75) {
      status = 'warning';
    }

    const systemMetrics = {
      timestamp: new Date().toISOString(),
      memory: {
        heapUsed: memUsage.heapUsed,
        heapTotal: memUsage.heapTotal,
        rss: memUsage.rss,
        external: memUsage.external,
        percentage: memoryPercentage
      },
      cpu: {
        user: cpuUsage.user,
        system: cpuUsage.system
      },
      uptime,
      status
    };

    return NextResponse.json(systemMetrics);
  } catch (error: any) {
    console.error('System metrics error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch system metrics', message: error.message },
      { status: 500 }
    );
  }
}
