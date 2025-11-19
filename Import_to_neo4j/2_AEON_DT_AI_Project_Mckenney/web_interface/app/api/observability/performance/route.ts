/**
 * Performance Observability API Endpoint
 *
 * Returns performance metrics from observability modules
 */

import { NextRequest, NextResponse } from 'next/server';
import { performanceMonitor } from '@/lib/observability/performance-monitor';

export async function GET(request: NextRequest) {
  try {
    // Generate real performance report
    const report = await performanceMonitor.generatePerformanceReport('1h');

    // Parse the report data
    const avgResponseTime = parseFloat(report.report.avgResponseTime) || 0;
    const p95ResponseTime = parseFloat(report.report.p95ResponseTime) || 0;
    const throughputMatch = report.report.throughput?.match(/(\d+)/);
    const throughput = throughputMatch ? parseInt(throughputMatch[1]) : 0;
    const errorRateMatch = report.report.errorRate?.match(/([\d.]+)/);
    const errorRate = errorRateMatch ? parseFloat(errorRateMatch[1]) : 0;

    const performanceMetrics = {
      avgResponseTime,
      p95ResponseTime,
      throughput,
      errorRate,
      generatedAt: report.generatedAt
    };

    return NextResponse.json(performanceMetrics);
  } catch (error: any) {
    console.error('Performance metrics error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch performance metrics', message: error.message },
      { status: 500 }
    );
  }
}
