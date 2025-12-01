/**
 * Agent Observability API Endpoint
 *
 * Returns agent activity metrics from observability tracker
 */

import { NextRequest, NextResponse } from 'next/server';
import { agentTracker } from '@/lib/observability/agent-tracker';

// In-memory storage for demo (will be replaced with Qdrant)
const agentActivityData = {
  activeAgents: 0,
  completedTasks: 0,
  failedTasks: 0,
  totalDuration: 0,
  taskCount: 0
};

export async function GET(request: NextRequest) {
  try {
    // Calculate average duration
    const averageDuration = agentActivityData.taskCount > 0
      ? agentActivityData.totalDuration / agentActivityData.taskCount
      : 0;

    const agentMetrics = {
      activeAgents: agentActivityData.activeAgents,
      completedTasks: agentActivityData.completedTasks,
      failedTasks: agentActivityData.failedTasks,
      averageDuration
    };

    return NextResponse.json(agentMetrics);
  } catch (error: any) {
    console.error('Agent metrics error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch agent metrics', message: error.message },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, agentId, duration, status } = body;

    // Update agent activity data based on action
    if (action === 'spawn') {
      agentActivityData.activeAgents++;
    } else if (action === 'complete') {
      agentActivityData.activeAgents = Math.max(0, agentActivityData.activeAgents - 1);

      if (status === 'success') {
        agentActivityData.completedTasks++;
      } else {
        agentActivityData.failedTasks++;
      }

      if (duration) {
        agentActivityData.totalDuration += duration;
        agentActivityData.taskCount++;
      }
    }

    return NextResponse.json({ success: true, data: agentActivityData });
  } catch (error: any) {
    console.error('Agent metrics update error:', error);
    return NextResponse.json(
      { error: 'Failed to update agent metrics', message: error.message },
      { status: 500 }
    );
  }
}
