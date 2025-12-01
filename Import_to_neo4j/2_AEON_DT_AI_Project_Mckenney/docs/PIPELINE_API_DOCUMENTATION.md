# Pipeline API Documentation

**Created**: 2025-11-11
**Last Updated**: 2025-11-11
**Status**: COMPLETE - Actual implementation documented

## Overview

The pipeline API implements a document processing workflow using an in-memory queue system. Documents flow through three sequential stages (Classification → NER → Ingestion) with persistent job tracking and progress monitoring.

---

## Architecture Summary

```
Request Flow:
  POST /api/pipeline/process
     ↓
  [Validation & Rate Limiting]
     ↓
  [Job Submission to In-Memory Queue]
     ↓
  Serial Processing (one job at a time)
     ↓
  GET /api/pipeline/status/[jobId]
     ↓
  [Return Job Status & Progress]
```

---

## 1. Job Submission: `/api/pipeline/process` (POST)

### Endpoint Details
- **Path**: `/api/pipeline/process`
- **Method**: `POST`
- **Authentication**: Required (Clerk auth)
- **Rate Limiting**: 100 requests per 15 minutes per IP

### Request Body Structure
```typescript
{
  files: Array<{
    path: string;        // File system path to document
    name: string;        // Human-readable filename
    size: number;        // File size in bytes
    type: string;        // MIME type (e.g., "application/pdf")
  }>,
  customer: string;      // Customer identifier
  tags: string[];        // Classification tags
  classification: {
    sector: string;      // Primary sector (required)
    subsector?: string;  // Secondary sector (optional)
  }
}
```

### Validation Rules
| Validation | Rule | Response |
|-----------|------|----------|
| Authentication | User must be authenticated | 401 Unauthorized |
| Files Array | At least one file required | 400 Bad Request |
| Customer | Required field | 400 Bad Request |
| Sector | Required in classification | 400 Bad Request |
| File Size | Max 100MB per file | 413 Payload Too Large |
| Rate Limit | 100 requests/15 min per IP | 429 Too Many Requests |

### Response (Success)
```json
{
  "success": true,
  "jobs": [
    {
      "jobId": "uuid-v4-string",
      "status": "queued",
      "progress": 0,
      "message": "Queued: filename.pdf",
      "fileName": "filename.pdf"
    }
  ],
  "message": "Started processing 1 file(s)"
}
```

### Job Queuing Process
1. For each file in request:
   - Generate unique UUID (jobId)
   - Create DocumentJobData object with all metadata
   - Call `addJob(jobData)` from documentQueue
2. Jobs are added to internal queue array (`jobQueue`)
3. Serial processor begins if not already running
4. Immediate response with queued status returned to client

---

## 2. Queue Implementation: `documentQueue.ts`

### Core Data Structures
```typescript
// In-memory storage
jobStore: Map<jobId, JobStatus>     // Persistent job tracking
jobQueue: DocumentJobData[]         // FIFO queue for processing
isProcessing: boolean               // Flag for serial processing lock
```

### Job Status Tracking
```typescript
interface JobStatus {
  jobId: string;
  fileName: string;
  status: 'queued' | 'classifying' | 'extracting' | 'ingesting' | 'complete' | 'failed';
  progress: number;                 // 0-100 percentage
  message: string;
  createdAt: string;                // ISO timestamp
  completedAt?: string;             // ISO timestamp when finished
  steps: {
    classification: { status: string; progress: number };
    ner: { status: string; progress: number };
    ingestion: { status: string; progress: number };
  };
  error?: string;
}
```

### Queue Management Functions

#### `addJob(jobData: DocumentJobData): Promise<string>`
**Purpose**: Add a new document to the processing queue

**Flow**:
1. Validates Python executable is available
2. Creates JobStatus object with initial state
3. Stores in jobStore Map
4. Appends to jobQueue array
5. Triggers `processQueue()` if not already running
6. Returns jobId

**Key Implementation**:
```typescript
// Job starts with this structure
{
  status: 'queued',
  progress: 0,
  message: 'Queued for processing',
  steps: {
    classification: { status: 'pending', progress: 0 },
    ner: { status: 'pending', progress: 0 },
    ingestion: { status: 'pending', progress: 0 }
  }
}
```

#### `processQueue(): Promise<void>`
**Purpose**: Serial processor - handles one job at a time

**Algorithm**:
```
WHILE jobQueue.length > 0:
  1. Set isProcessing = true (acquire lock)
  2. Shift first job from queue
  3. Call processDocumentJob()
  4. Log completion
  5. Continue to next job
  6. Set isProcessing = false (release lock)
```

**Key Property**: Only ONE job processes at a time. Others wait in queue.

#### `processDocumentJob(jobData): Promise<void>`
**Purpose**: Execute the three-stage processing pipeline

**Stage 1: Classification (10% → 40%)**
```typescript
updateJobStatus(jobId, 'classifying', 10, 'Starting document classification');

await runPythonAgent('classifier_agent.py', {
  file_path: filePath,
  sector: classification.sector,
  subsector: classification.subsector
});

updateJobStatus(jobId, 'extracting', 40, 'Classification complete...');
```

**Stage 2: NER/Entity Extraction (40% → 70%)**
```typescript
await runPythonAgent('ner_agent.py', {
  file_path: filePath,
  customer: customer
});

updateJobStatus(jobId, 'ingesting', 70, 'Entity extraction complete...');
```

**Stage 3: Neo4j Ingestion (70% → 100%)**
```typescript
await runPythonAgent('ingestion_agent.py', {
  file_path: filePath,
  customer: customer,
  tags: tags,
  classification: classification
});

updateJobStatus(jobId, 'complete', 100, 'Processing complete');
```

**Error Handling**:
- Any stage failure catches error
- Updates job status to 'failed' with error message
- Re-throws error for logging
- Previous stages' results may persist in Neo4j

---

## 3. Python Agent Invocation: `runPythonAgent()`

### Execution Model
```typescript
function runPythonAgent(scriptName: string, args: any): Promise<void>
```

### Process Invocation
```javascript
const pythonProcess = spawn(pythonPath, [scriptPath, JSON.stringify(args)])
```

**Parameters**:
- `pythonPath`: From `PYTHON_PATH` env var, defaults to `python3`
- `scriptPath`: `${AGENTS_PATH}/${scriptName}`
- `args`: JSON-stringified object passed as command-line argument

### Python Agent Scripts
| Agent | Trigger | Arguments |
|-------|---------|-----------|
| `classifier_agent.py` | Classification stage | `file_path`, `sector`, `subsector` |
| `ner_agent.py` | Extraction stage | `file_path`, `customer` |
| `ingestion_agent.py` | Ingestion stage | `file_path`, `customer`, `tags`, `classification` |

### Timeout Handling
```typescript
const TIMEOUT_MS = 5 * 60 * 1000; // 5 minutes

setTimeout(() => {
  pythonProcess.kill('SIGTERM');
  reject(new Error(`${scriptName} timed out after 5 minutes`));
}, TIMEOUT_MS);
```

**Behavior**:
- Each agent has 5-minute maximum execution time
- If exceeded: process killed, job marked failed
- Timeout applies per agent, not per document

### Output Capture
```typescript
pythonProcess.stdout.on('data', (data) => {
  console.log(`[${scriptName}] ${data}`);
});

pythonProcess.stderr.on('data', (data) => {
  console.error(`[${scriptName}] ${data}`);
});
```

**Implementation**: All stdout/stderr logged to console for debugging

---

## 4. Progress Tracking: `updateJobStatus()`

### Progress Mapping
```typescript
Progress → Status Mapping:
0%        → 'queued' + all steps 'pending'
10%       → 'classifying' + classification running
40%       → 'extracting' + classification complete, NER running
70%       → 'ingesting' + NER complete, ingestion running
100%      → 'complete' + all steps complete

steps[].progress:
  0    → 'pending'
  50   → 'running'
  100  → 'complete'
```

### Update Mechanism
```typescript
function updateJobStatus(
  jobId: string,
  status: JobStatus['status'],
  progress: number,           // 0-100
  message: string,
  error?: string
): void
```

**Implementation**:
1. Retrieves current job from jobStore
2. Merges with new status
3. Calculates step progress based on overall progress
4. Adds completedAt timestamp if status is 'complete' or 'failed'
5. Stores updated job back to jobStore
6. Logs to console

**Step Progress Logic**:
```typescript
classification: {
  status: progress >= 40 ? 'complete' : progress >= 10 ? 'running' : 'pending',
  progress: progress >= 40 ? 100 : progress >= 10 ? 50 : 0
},
ner: {
  status: progress >= 70 ? 'complete' : progress >= 40 ? 'running' : 'pending',
  progress: progress >= 70 ? 100 : progress >= 40 ? 50 : 0
},
ingestion: {
  status: progress >= 100 ? 'complete' : progress >= 70 ? 'running' : 'pending',
  progress: progress >= 100 ? 100 : progress >= 70 ? 50 : 0
}
```

---

## 5. Status Retrieval: `/api/pipeline/status/[jobId]`

### Endpoint Details
- **Path**: `/api/pipeline/status/[jobId]`
- **Method**: `GET`
- **Authentication**: None (note: security issue - should require auth)
- **Rate Limiting**: None currently

### Response (Success)
```json
{
  "success": true,
  "jobId": "uuid-string",
  "fileName": "document.pdf",
  "status": "extracting",
  "progress": 45,
  "message": "Classification complete, starting entity extraction",
  "createdAt": "2025-11-11T10:30:00Z",
  "completedAt": null,
  "customer": "customer-name",
  "tags": ["tag1", "tag2"],
  "classification": {
    "sector": "healthcare",
    "subsector": "medical"
  },
  "steps": {
    "classification": { "status": "complete", "progress": 100 },
    "ner": { "status": "running", "progress": 50 },
    "ingestion": { "status": "pending", "progress": 0 }
  }
}
```

### Response (Job Not Found)
```json
{ "error": "Job not found" }
// Status: 404
```

---

## 6. Queue Status: GET `/api/pipeline/process?jobId=none`

### Overview Status (No jobId parameter)
```json
{
  "success": true,
  "jobs": [],
  "queueStatus": {
    "waiting": 5,      // Jobs in queue not yet started
    "active": 1,       // Jobs currently processing
    "completed": 23,   // Successfully completed jobs
    "failed": 2,       // Failed jobs
    "delayed": 0,      // Currently 0 (not implemented)
    "total": 31        // Sum of all jobs in system
  }
}
```

**Calculation**:
```typescript
waiting = jobQueue.length
active = isProcessing ? 1 : 0
completed = count(job.status === 'complete')
failed = count(job.status === 'failed')
total = waiting + active + completed + failed
```

---

## 7. Error Handling

### API Error Responses

| Error | Status | Response |
|-------|--------|----------|
| Missing auth | 401 | `{ error: 'Unauthorized' }` |
| No files | 400 | `{ error: 'No files provided' }` |
| Missing customer/sector | 400 | `{ error: 'Customer and classification sector are required' }` |
| File > 100MB | 413 | `{ error: 'File exceeds maximum size of 100MB', details: '...'}` |
| Rate limit exceeded | 429 | `{ error: 'Rate limit exceeded. Try again later.' }` |
| Job not found | 404 | `{ error: 'Job not found' }` |
| Server error | 500 | `{ error: 'Failed to submit for processing', details: '...' }` |

### Job Processing Errors

**Classification Failure**:
```
Status: 'failed'
Progress: 0
Message: 'Processing failed: [error details]'
Error: Captured and stored
```

**NER Failure**:
```
Status: 'failed'
Progress: 0
Message: 'Processing failed: [error details]'
Note: Classification already ran but results not ingested
```

**Ingestion Failure**:
```
Status: 'failed'
Progress: 0
Message: 'Processing failed: [error details]'
Note: Classification & NER results exist but Neo4j graph not updated
```

---

## 8. Security Measures

### Path Validation
```typescript
function validateFilePath(filePath: string): boolean {
  const normalized = path.normalize(filePath);
  const allowedDir = path.resolve(process.env.UPLOAD_DIR || '/uploads');
  
  // Check for directory traversal (..)
  if (normalized.includes('..')) return false;
  
  // Verify file within allowed directory
  if (!resolvedPath.startsWith(allowedDir)) return false;
  
  return true;
}
```

**Protection**: Prevents reading files outside upload directory

### Rate Limiting
```typescript
const requestCounts = new Map<ip, { count, resetTime }>()

function checkRateLimit(ip: string): boolean {
  limit: 100 requests
  window: 15 minutes
  // Per-IP tracking with sliding window
}
```

**Implementation**: In-memory tracker per IP address

### Authentication
```typescript
const { userId } = await auth();  // Clerk authentication
if (!userId) return 401;
```

**Applied to**: POST, GET, DELETE endpoints

### Environment Validation
```typescript
// Validates Python executable exists before processing
await validatePythonPath()
// Throws error if python3 unavailable
```

---

## 9. Environment Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `PYTHON_PATH` | `python3` | Python executable location |
| `AGENTS_PATH` | `../agents` | Directory containing Python agents |
| `UPLOAD_DIR` | `/uploads` | Safe directory for uploaded files |

**Validation**: Python path validated on each addJob() call

---

## 10. Processing Workflow Example

### Timeline for Single Document
```
T+0s:   POST /api/pipeline/process
        ↓ validation & rate limit check
        ↓ job created with UUID
        ↓ added to jobQueue
        ↓ processQueue() triggered
        ↓ response: { jobId, status: 'queued', progress: 0 }

T+0.5s: processQueue() begins processing
        ↓ shift job from queue
        ↓ status: 'classifying' (10%)

T+0.5-5.5s: classifier_agent.py runs (0-5 min timeout)
        ↓ processes document
        ↓ generates classification results

T+5.5s: classification complete
        ↓ status: 'extracting' (40%)
        ↓ ner_agent.py starts

T+5.5-10.5s: ner_agent.py runs
        ↓ extracts named entities
        ↓ generates relationship data

T+10.5s: NER complete
        ↓ status: 'ingesting' (70%)
        ↓ ingestion_agent.py starts

T+10.5-15.5s: ingestion_agent.py runs
        ↓ writes entities to Neo4j
        ↓ creates relationships

T+15.5s: Complete
        ↓ status: 'complete' (100%)
        ↓ completedAt: ISO timestamp
        ↓ next job in queue begins (or system idle)
```

### Concurrent Requests Example
```
Request 1 (file1.pdf):    T+0  → Queue position 1
Request 2 (file2.pdf):    T+0.1 → Queue position 2
Request 3 (file3.pdf):    T+0.2 → Queue position 3

Processing:
T+0-15s:   File 1 processes
T+15-30s:  File 2 processes
T+30-45s:  File 3 processes

Status polling:
GET /api/pipeline/status/job1 → Running (55%)
GET /api/pipeline/status/job2 → Queued (0%)
GET /api/pipeline/status/job3 → Queued (0%)
GET /api/pipeline/process     → waiting: 2, active: 1, completed: 0
```

---

## 11. Known Limitations

| Limitation | Impact | Workaround |
|-----------|--------|-----------|
| In-memory storage | Data lost on server restart | Implement Redis persistence |
| Serial processing | Only 1 file at a time | Consider parallel processing pools |
| No job persistence | Cannot resume after crash | Add database storage |
| Rate limit in-memory | Resets per server instance | Use distributed cache (Redis) |
| Status route no auth | Security risk | Add Clerk auth check |
| 5-min timeout | Long documents fail | Increase or make configurable |
| No job cancellation | Jobs run to completion | Implement signal handling |
| No job history | Can't audit past jobs | Add database audit trail |

---

## 12. Integration Points

### Depends On
- **Clerk Authentication**: User identity verification
- **Python 3**: Agent execution environment
- **Python Agents**: classifier_agent.py, ner_agent.py, ingestion_agent.py
- **Neo4j**: Graph database for final ingestion

### Consumed By
- **Web Interface**: Frontend for job submission
- **Status Dashboard**: Real-time progress tracking
- **Analytics**: Job metrics and performance

---

## Summary

The pipeline implements a **serial, in-memory document processing system** with three stages:

1. **Document Classification** (10-40%)
2. **Named Entity Recognition via NER v9** (40-70%)
3. **Neo4j Graph Ingestion** (70-100%)

Each job processes completely before the next begins, with persistent status tracking and detailed progress reporting. Python agents handle actual ML processing, invoked via child processes with 5-minute timeouts.

**Architecture**: Request → Queue → Serial Processing → Status Tracking
**Storage**: In-memory Maps (jobs lost on restart)
**Concurrency**: FIFO serial queue
**Scalability**: Limited by single-process bottleneck

