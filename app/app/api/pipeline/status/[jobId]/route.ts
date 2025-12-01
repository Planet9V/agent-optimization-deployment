import { NextRequest, NextResponse } from 'next/server';
import { jobs } from '../../process/route';

/**
 * GET /api/pipeline/status/[jobId]
 * Retrieves current processing status for a specific job
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { jobId: string } }
) {
  try {
    const { jobId } = params;

    // Input validation
    if (!jobId || typeof jobId !== 'string') {
      return NextResponse.json(
        { success: false, error: 'Invalid job ID' },
        { status: 400 }
      );
    }

    const job = jobs.get(jobId);

    if (!job) {
      return NextResponse.json(
        { success: false, error: 'Job not found' },
        { status: 404 }
      );
    }

    // Return job status with all relevant information
    return NextResponse.json({
      success: true,
      jobId: job.jobId,
      fileName: job.fileName,
      status: job.status,
      progress: job.progress,
      message: job.message,
      createdAt: job.createdAt,
      steps: {
        classification: {
          status: job.steps.classification.status,
          progress: job.steps.classification.progress,
          error: job.steps.classification.error
        },
        ner: {
          status: job.steps.ner.status,
          progress: job.steps.ner.progress,
          error: job.steps.ner.error
        },
        ingestion: {
          status: job.steps.ingestion.status,
          progress: job.steps.ingestion.progress,
          error: job.steps.ingestion.error
        }
      },
      // Additional metadata
      customer: job.customer,
      tags: job.tags,
      classification: job.classification
    });

  } catch (error: any) {
    console.error('Status check error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

/**
 * GET /api/pipeline/status (without jobId)
 * Retrieves all jobs (optional feature for admin dashboard)
 */
export async function GET_ALL(request: NextRequest) {
  try {
    const allJobs = Array.from(jobs.values()).map(job => ({
      jobId: job.jobId,
      fileName: job.fileName,
      status: job.status,
      progress: job.progress,
      message: job.message,
      createdAt: job.createdAt,
      customer: job.customer
    }));

    return NextResponse.json({
      success: true,
      jobs: allJobs,
      total: allJobs.length
    });

  } catch (error: any) {
    console.error('Status list error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}
