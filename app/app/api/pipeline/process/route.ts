import { NextRequest, NextResponse } from 'next/server';
import { v4 as uuidv4 } from 'uuid';

// Type definitions
interface FileInput {
  originalName: string;
  path: string;
  size: number;
  mimeType: string;
}

interface ProcessRequest {
  files: FileInput[];
  customer: string;
  tags: string[];
  classification: string;
}

interface JobStep {
  status: 'pending' | 'running' | 'complete' | 'failed';
  progress: number;
  error?: string;
}

interface Job {
  jobId: string;
  fileName: string;
  status: 'queued' | 'classifying' | 'extracting' | 'ingesting' | 'complete' | 'failed';
  progress: number;
  message: string;
  createdAt: string;
  file: FileInput;
  customer: string;
  tags: string[];
  classification: string;
  steps: {
    classification: JobStep;
    ner: JobStep;
    ingestion: JobStep;
  };
}

// In-memory job store (will be replaced with PostgreSQL per TASK-003)
export const jobs = new Map<string, Job>();

/**
 * POST /api/pipeline/process
 * Initiates document processing pipeline for uploaded files
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json() as ProcessRequest;
    const { files, customer, tags, classification } = body;

    // Input validation
    if (!files || !Array.isArray(files) || files.length === 0) {
      return NextResponse.json(
        { success: false, error: 'No files provided' },
        { status: 400 }
      );
    }

    if (!customer || typeof customer !== 'string') {
      return NextResponse.json(
        { success: false, error: 'Customer name is required' },
        { status: 400 }
      );
    }

    const createdJobs = files.map((file: FileInput) => {
      const jobId = uuidv4();
      const job: Job = {
        jobId,
        fileName: file.originalName,
        status: 'queued',
        progress: 0,
        message: `Queued: ${file.originalName}`,
        createdAt: new Date().toISOString(),
        file,
        customer,
        tags: tags || [],
        classification: classification || 'auto',
        steps: {
          classification: { status: 'pending', progress: 0 },
          ner: { status: 'pending', progress: 0 },
          ingestion: { status: 'pending', progress: 0 }
        }
      };

      jobs.set(jobId, job);

      // Start async processing (no await to immediately return response)
      processJob(jobId).catch(error => {
        console.error(`Job ${jobId} processing error:`, error);
        const failedJob = jobs.get(jobId);
        if (failedJob) {
          failedJob.status = 'failed';
          failedJob.message = `Processing failed: ${error.message}`;
          jobs.set(jobId, failedJob);
        }
      });

      return {
        jobId,
        status: 'queued',
        progress: 0,
        fileName: file.originalName
      };
    });

    return NextResponse.json({
      success: true,
      jobs: createdJobs,
      message: `Started processing ${files.length} file(s)`
    });
  } catch (error: any) {
    console.error('Pipeline process error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

/**
 * Simulates asynchronous document processing pipeline
 * Steps: Classification → NER → Ingestion
 */
async function processJob(jobId: string): Promise<void> {
  const job = jobs.get(jobId);
  if (!job) {
    throw new Error(`Job ${jobId} not found`);
  }

  try {
    // Step 1: Document Classification
    job.status = 'classifying';
    job.progress = 10;
    job.message = 'Analyzing document type...';
    job.steps.classification = { status: 'running', progress: 50 };
    jobs.set(jobId, job);

    // Simulate classification processing
    await new Promise(resolve => setTimeout(resolve, 3000));

    job.progress = 40;
    job.message = 'Classification complete';
    job.steps.classification = { status: 'complete', progress: 100 };
    jobs.set(jobId, job);

    // Step 2: Named Entity Recognition (NER)
    job.status = 'extracting';
    job.progress = 45;
    job.message = 'Extracting entities...';
    job.steps.ner = { status: 'running', progress: 50 };
    jobs.set(jobId, job);

    // Simulate NER processing
    await new Promise(resolve => setTimeout(resolve, 5000));

    job.progress = 70;
    job.message = 'Entity extraction complete';
    job.steps.ner = { status: 'complete', progress: 100 };
    jobs.set(jobId, job);

    // Step 3: Knowledge Graph Ingestion
    job.status = 'ingesting';
    job.progress = 75;
    job.message = 'Ingesting into knowledge graph...';
    job.steps.ingestion = { status: 'running', progress: 50 };
    jobs.set(jobId, job);

    // Simulate ingestion processing
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Job complete
    job.status = 'complete';
    job.progress = 100;
    job.message = 'Processing complete';
    job.steps.ingestion = { status: 'complete', progress: 100 };
    jobs.set(jobId, job);

  } catch (error: any) {
    console.error(`Job ${jobId} processing error:`, error);
    job.status = 'failed';
    job.message = `Processing failed: ${error.message}`;

    // Mark current step as failed
    const currentStep = job.status === 'classifying' ? 'classification'
      : job.status === 'extracting' ? 'ner'
      : 'ingestion';

    job.steps[currentStep] = {
      status: 'failed',
      progress: job.steps[currentStep].progress,
      error: error.message
    };

    jobs.set(jobId, job);
    throw error;
  }
}
