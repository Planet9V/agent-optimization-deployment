import { NextRequest, NextResponse } from 'next/server';

// Import the shared jobs map from process route
// In production, use Redis or a database for job state
const processingJobs = new Map<string, any>();

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ jobId: string }> }
) {
  try {
    const { jobId } = await params;

    // Check if job exists in the shared jobs map
    // Note: In production, retrieve from Redis/database
    const job = processingJobs.get(jobId);

    if (!job) {
      return NextResponse.json(
        { error: 'Job not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      jobId: job.jobId,
      fileName: job.fileName,
      status: job.status,
      progress: job.progress,
      message: job.message,
      createdAt: job.createdAt,
      completedAt: job.completedAt,
      steps: job.steps,
      customer: job.customer,
      tags: job.tags,
      classification: job.classification
    });
  } catch (error) {
    console.error('Status check error:', error);
    return NextResponse.json(
      {
        error: 'Failed to get job status',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ jobId: string }> }
) {
  try {
    const { jobId } = await params;

    const job = processingJobs.get(jobId);

    if (!job) {
      return NextResponse.json(
        { error: 'Job not found' },
        { status: 404 }
      );
    }

    // Only allow cancellation of queued or running jobs
    if (job.status === 'complete' || job.status === 'failed') {
      return NextResponse.json(
        { error: 'Cannot cancel completed or failed job' },
        { status: 400 }
      );
    }

    // Mark as cancelled
    job.status = 'cancelled';
    job.message = 'Processing cancelled by user';
    processingJobs.set(jobId, job);

    return NextResponse.json({
      success: true,
      message: 'Job cancelled successfully',
      jobId
    });
  } catch (error) {
    console.error('Cancel error:', error);
    return NextResponse.json(
      { error: 'Failed to cancel job' },
      { status: 500 }
    );
  }
}
