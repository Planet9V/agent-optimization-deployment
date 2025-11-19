/**
 * Document Processing API Route
 * Redis + BullMQ implementation for persistent, distributed job queue
 */

import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import { v4 as uuidv4 } from 'uuid';
import {
  addJob,
  getJobStatus,
  getQueueStatus,
  type DocumentJobData,
} from '@/lib/queue/documentQueue';

interface ProcessingRequest {
  files: Array<{
    path: string;
    name: string;
    size: number;
    type: string;
  }>;
  customer: string;
  tags: string[];
  classification: {
    sector: string;
    subsector?: string;
  };
}

// File size validation constants and function
const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100MB in bytes

function validateFileSize(fileSize: number): boolean {
  return fileSize <= MAX_FILE_SIZE;
}

function formatFileSize(bytes: number): string {
  const mb = bytes / (1024 * 1024);
  return `${mb.toFixed(2)}MB`;
}

// Simple rate limiting (in-memory tracker)
const requestCounts = new Map<string, { count: number; resetTime: number }>();

function checkRateLimit(ip: string): boolean {
  const now = Date.now();
  const limit = 100; // requests
  const window = 15 * 60 * 1000; // 15 minutes in ms

  const record = requestCounts.get(ip);

  if (!record || now > record.resetTime) {
    requestCounts.set(ip, { count: 1, resetTime: now + window });
    return true;
  }

  if (record.count >= limit) {
    return false; // Rate limit exceeded
  }

  record.count++;
  return true;
}

// Worker is automatically managed by the in-memory queue

export async function POST(request: NextRequest) {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Rate limiting
  const ip = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown';
  if (!checkRateLimit(ip)) {
    return NextResponse.json({ error: 'Rate limit exceeded. Try again later.' }, { status: 429 });
  }

  try {
    const body: ProcessingRequest = await request.json();

    // Validation
    if (!body.files || body.files.length === 0) {
      return NextResponse.json(
        { error: 'No files provided' },
        { status: 400 }
      );
    }

    if (!body.customer || !body.classification.sector) {
      return NextResponse.json(
        { error: 'Customer and classification sector are required' },
        { status: 400 }
      );
    }

    // Validate file sizes to prevent memory exhaustion
    for (const file of body.files) {
      if (file.size && !validateFileSize(file.size)) {
        return NextResponse.json(
          {
            error: `File "${file.name}" exceeds maximum size of 100MB`,
            details: `File size: ${formatFileSize(file.size)}, Maximum allowed: ${formatFileSize(MAX_FILE_SIZE)}`,
          },
          { status: 413 } // 413 Payload Too Large
        );
      }
    }

    // Create in-memory queue jobs for each file
    const jobs = await Promise.all(
      body.files.map(async (file) => {
        const jobId = uuidv4();

        const jobData: DocumentJobData = {
          jobId,
          fileName: file.name,
          filePath: file.path,
          customer: body.customer,
          tags: body.tags,
          classification: body.classification,
          fileSize: file.size,
          fileType: file.type,
        };

        // Add job to in-memory queue
        const addedJobId = await addJob(jobData);

        return {
          jobId: addedJobId,
          status: 'queued',
          progress: 0,
          message: `Queued: ${file.name}`,
          fileName: file.name,
        };
      })
    );

    return NextResponse.json({
      success: true,
      jobs,
      message: `Started processing ${jobs.length} file(s)`,
    });
  } catch (error) {
    console.error('Process submission error:', error);
    return NextResponse.json(
      {
        error: 'Failed to submit for processing',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Rate limiting
  const ip = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown';
  if (!checkRateLimit(ip)) {
    return NextResponse.json({ error: 'Rate limit exceeded. Try again later.' }, { status: 429 });
  }

  try {
    const { searchParams } = new URL(request.url);
    const jobId = searchParams.get('jobId');

    // If jobId is provided, return specific job status
    if (jobId) {
      const status = await getJobStatus(jobId);

      if (!status) {
        return NextResponse.json(
          { error: 'Job not found' },
          { status: 404 }
        );
      }

      return NextResponse.json({
        success: true,
        job: status,
      });
    }

    // Get queue status from in-memory queue
    const queueStatus = await getQueueStatus();

    return NextResponse.json({
      success: true,
      jobs: [],
      queueStatus,
    });
  } catch (error) {
    console.error('Job retrieval error:', error);
    return NextResponse.json(
      {
        error: 'Failed to retrieve jobs',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}

// Optional: DELETE endpoint to remove specific jobs
export async function DELETE(request: NextRequest) {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Rate limiting
  const ip = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown';
  if (!checkRateLimit(ip)) {
    return NextResponse.json({ error: 'Rate limit exceeded. Try again later.' }, { status: 429 });
  }

  try {
    const { searchParams } = new URL(request.url);
    const jobId = searchParams.get('jobId');

    if (!jobId) {
      return NextResponse.json(
        { error: 'Job ID required' },
        { status: 400 }
      );
    }

    // In-memory queue doesn't support removal yet
    // Return success for now
    return NextResponse.json({
      success: true,
      message: `Job removal not yet implemented for in-memory queue`,
    });
  } catch (error) {
    console.error('Job deletion error:', error);
    return NextResponse.json(
      {
        error: 'Failed to delete job',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}
