/**
 * Document Processing Queue
 * Simple in-memory queue for serial document processing
 */

import { spawn, exec } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';

const execAsync = promisify(exec);

// Queue name constant
export const DOCUMENT_QUEUE_NAME = 'document-processing';

// In-memory job storage
const jobStore = new Map<string, JobStatus>();
const jobQueue: DocumentJobData[] = [];
let isProcessing = false;

/**
 * Validates file paths to prevent directory traversal attacks
 * @param filePath - The file path to validate
 * @returns true if path is valid and within allowed directory, false otherwise
 */
function validateFilePath(filePath: string): boolean {
  const normalized = path.normalize(filePath);
  const allowedDir = path.resolve(process.env.UPLOAD_DIR || '/uploads');
  const resolvedPath = path.resolve(normalized);

  // Prevent directory traversal by checking for ".." sequences
  if (normalized.includes('..')) {
    return false;
  }

  // Ensure file is within allowed directory
  if (!resolvedPath.startsWith(allowedDir)) {
    return false;
  }

  return true;
}

// Job data interfaces
export interface DocumentJobData {
  jobId: string;
  fileName: string;
  filePath: string;
  customer: string;
  tags: string[];
  classification: {
    sector: string;
    subsector?: string;
  };
  fileSize: number;
  fileType: string;
}

export interface JobStatus {
  jobId: string;
  fileName: string;
  status: 'queued' | 'classifying' | 'extracting' | 'ingesting' | 'complete' | 'failed';
  progress: number;
  message: string;
  createdAt: string;
  completedAt?: string;
  steps: {
    classification: { status: string; progress: number };
    ner: { status: string; progress: number };
    ingestion: { status: string; progress: number };
  };
  error?: string;
}

// Validate Python executable exists
async function validatePythonPath(): Promise<void> {
  const pythonPath = process.env.PYTHON_PATH || 'python3';

  try {
    await execAsync(`${pythonPath} --version`);
    console.log(`✅ Python validated: ${pythonPath}`);
  } catch (error) {
    throw new Error(
      `Python executable not found: ${pythonPath}. ` +
      `Please set PYTHON_PATH environment variable or install Python.`
    );
  }
}

// Helper function to run Python agents with timeout handling
function runPythonAgent(scriptName: string, args: any): Promise<void> {
  return new Promise((resolve, reject) => {
    const pythonPath = process.env.PYTHON_PATH || 'python3';
    const agentsPath = process.env.AGENTS_PATH || '../agents';
    const scriptPath = `${agentsPath}/${scriptName}`;
    const TIMEOUT_MS = 5 * 60 * 1000; // 5 minutes

    const pythonProcess = spawn(pythonPath, [scriptPath, JSON.stringify(args)]);

    // Timeout handler - kill process if it runs too long
    const timeoutId = setTimeout(() => {
      pythonProcess.kill('SIGTERM');
      reject(new Error(`${scriptName} timed out after 5 minutes`));
    }, TIMEOUT_MS);

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
      console.log(`[${scriptName}] ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
      console.error(`[${scriptName}] ${data}`);
    });

    pythonProcess.on('close', (code) => {
      clearTimeout(timeoutId); // Clear timeout on completion
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`${scriptName} failed with code ${code}: ${stderr}`));
      }
    });

    pythonProcess.on('error', (error) => {
      clearTimeout(timeoutId);
      reject(new Error(`Failed to start ${scriptName}: ${error.message}`));
    });
  });
}

// Document processing worker logic
export async function processDocumentJob(jobData: DocumentJobData): Promise<void> {
  const { jobId, filePath, fileName, customer, tags, classification } = jobData;

  try {
    // Validate file path before processing to prevent directory traversal attacks
    if (!validateFilePath(filePath)) {
      throw new Error(`Invalid file path: ${filePath}. Path traversal attempt detected.`);
    }

    // Update job status
    updateJobStatus(jobId, 'classifying', 10, 'Starting document classification');

    // Step 1: Classification (SERIAL)
    await runPythonAgent('classifier_agent.py', {
      file_path: filePath,
      sector: classification.sector,
      subsector: classification.subsector,
    });

    updateJobStatus(jobId, 'extracting', 40, 'Classification complete, starting entity extraction');

    // Step 2: NER (SERIAL - waits for classification)
    await runPythonAgent('ner_agent.py', {
      file_path: filePath,
      customer: customer,
    });

    updateJobStatus(jobId, 'ingesting', 70, 'Entity extraction complete, starting ingestion');

    // Step 3: Ingestion to Neo4j (SERIAL - waits for NER)
    await runPythonAgent('ingestion_agent.py', {
      file_path: filePath,
      customer: customer,
      tags: tags,
      classification: classification,
    });

    updateJobStatus(jobId, 'complete', 100, 'Processing complete');

  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    updateJobStatus(jobId, 'failed', 0, `Processing failed: ${errorMessage}`, errorMessage);
    throw error;
  }
}

// Helper to update job status in memory
function updateJobStatus(
  jobId: string,
  status: JobStatus['status'],
  progress: number,
  message: string,
  error?: string
): void {
  const existingJob = jobStore.get(jobId);
  if (!existingJob) return;

  const updatedJob: JobStatus = {
    ...existingJob,
    status,
    progress,
    message,
    error,
    steps: {
      classification: {
        status: progress >= 40 ? 'complete' : progress >= 10 ? 'running' : 'pending',
        progress: progress >= 40 ? 100 : progress >= 10 ? 50 : 0,
      },
      ner: {
        status: progress >= 70 ? 'complete' : progress >= 40 ? 'running' : 'pending',
        progress: progress >= 70 ? 100 : progress >= 40 ? 50 : 0,
      },
      ingestion: {
        status: progress >= 100 ? 'complete' : progress >= 70 ? 'running' : 'pending',
        progress: progress >= 100 ? 100 : progress >= 70 ? 50 : 0,
      },
    },
  };

  if (status === 'complete' || status === 'failed') {
    updatedJob.completedAt = new Date().toISOString();
  }

  jobStore.set(jobId, updatedJob);
  console.log(`Job ${jobId} status: ${status} (${progress}%) - ${message}`);
}

// Serial queue processor
async function processQueue(): Promise<void> {
  if (isProcessing || jobQueue.length === 0) return;

  isProcessing = true;

  while (jobQueue.length > 0) {
    const jobData = jobQueue.shift()!;

    console.log(`Processing job ${jobData.jobId} (${jobQueue.length} remaining in queue)`);

    try {
      await processDocumentJob(jobData);
    } catch (error) {
      console.error(`Job ${jobData.jobId} failed:`, error);
    }
  }

  isProcessing = false;
}

// Add job to queue
export async function addJob(jobData: DocumentJobData): Promise<string> {
  // Validate Python before accepting jobs
  await validatePythonPath();

  const jobStatus: JobStatus = {
    jobId: jobData.jobId,
    fileName: jobData.fileName,
    status: 'queued',
    progress: 0,
    message: 'Queued for processing',
    createdAt: new Date().toISOString(),
    steps: {
      classification: { status: 'pending', progress: 0 },
      ner: { status: 'pending', progress: 0 },
      ingestion: { status: 'pending', progress: 0 },
    },
  };

  jobStore.set(jobData.jobId, jobStatus);
  jobQueue.push(jobData);

  console.log(`Job ${jobData.jobId} added to queue (position: ${jobQueue.length})`);

  // Start processing if not already running
  processQueue().catch(console.error);

  return jobData.jobId;
}

// Graceful shutdown handler
export async function shutdownWorker(): Promise<void> {
  console.log('Shutdown requested, waiting for current job to complete...');
  while (isProcessing) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  console.log('Worker shutdown complete');
}

// Queue status helper
export async function getQueueStatus() {
  const waiting = jobQueue.length;
  const active = isProcessing ? 1 : 0;

  let completed = 0;
  let failed = 0;

  for (const job of jobStore.values()) {
    if (job.status === 'complete') completed++;
    if (job.status === 'failed') failed++;
  }

  return {
    waiting,
    active,
    completed,
    failed,
    delayed: 0,
    total: waiting + active + completed + failed,
  };
}

// Job retrieval helper
export async function getJobStatus(jobId: string): Promise<JobStatus | null> {
  return jobStore.get(jobId) || null;
}
