# ETL Pipeline - Serial Job Processing with Python Agents

**File**: 03_ETL_PIPELINE.md
**Created**: 2025-11-11
**Modified**: 2025-11-11
**Version**: 1.0.0
**Purpose**: Document processing pipeline architecture with in-memory queue and Python agents
**Status**: ACTIVE

## Executive Summary

The AEON DT AI Project uses an **in-memory serial processing pipeline** (NOT BullMQ) that executes three Python agents sequentially for each uploaded document. Jobs are processed one at a time through classification, entity extraction (NER), and Neo4j ingestion stages.

**Architecture**: In-Memory Map Queue → Serial Processing → 3 Python Agents → Neo4j Storage

**Processing Model**: FIFO Serial Queue (one job at a time)

**Storage**: In-memory job tracking (jobs lost on server restart)

**Note**: This is a simplified implementation. Production systems should use Redis-backed queues like BullMQ for persistence and parallel processing.

---

## Current Implementation Architecture

### System Overview
```
┌────────────────────────────────────────────────────────────┐
│              Document Processing Pipeline                   │
└────────────────────────────────────────────────────────────┘

POST /api/pipeline/process
   ↓
┌─────────────────────────────────────────┐
│  Document Queue (In-Memory)             │
│  - jobStore: Map<jobId, JobStatus>      │
│  - jobQueue: DocumentJobData[]          │
│  - isProcessing: boolean                │
└─────────────────────────────────────────┘
   ↓
Serial Processing Loop (processQueue())
   ↓
┌─────────────────────────────────────────┐
│  Agent 1: classifier_agent.py           │
│  Progress: 10% → 40%                    │
│  Timeout: 5 minutes                     │
└─────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────┐
│  Agent 2: ner_agent.py                  │
│  Progress: 40% → 70%                    │
│  Timeout: 5 minutes                     │
└─────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────┐
│  Agent 3: ingestion_agent.py            │
│  Progress: 70% → 100%                   │
│  Timeout: 5 minutes                     │
└─────────────────────────────────────────┘
   ↓
Neo4j Knowledge Graph
   - Document nodes
   - Entity nodes
   - Relationship edges
   - Metadata properties
```

---

## Queue Implementation

### File Location
**Component**: `/web_interface/lib/queue/documentQueue.ts`

### Core Data Structures

#### In-Memory Storage
```typescript
// Persistent job tracking across all sessions
const jobStore = new Map<string, JobStatus>();

// FIFO queue for pending jobs
const jobQueue: DocumentJobData[] = [];

// Processing lock (prevents concurrent processing)
let isProcessing = false;
```

#### Job Data Structure
```typescript
interface DocumentJobData {
  jobId: string;              // UUID v4
  fileName: string;           // Original filename
  filePath: string;           // MinIO path (uploads/YYYY-MM-DD_HH-MM-SS_filename.ext)
  customer: string;           // Customer identifier
  tags: string[];             // Metadata tags
  classification: {
    sector: string;           // Required sector
    subsector?: string;       // Optional subsector
  };
  fileSize: number;           // Bytes
  fileType: string;           // MIME type
}
```

#### Job Status Tracking
```typescript
interface JobStatus {
  jobId: string;
  fileName: string;
  status: 'queued' | 'classifying' | 'extracting' | 'ingesting' | 'complete' | 'failed';
  progress: number;                 // 0-100
  message: string;
  createdAt: string;                // ISO 8601 timestamp
  completedAt?: string;             // ISO 8601 timestamp
  steps: {
    classification: {
      status: 'pending' | 'running' | 'complete';
      progress: number;             // 0, 50, or 100
    };
    ner: {
      status: 'pending' | 'running' | 'complete';
      progress: number;
    };
    ingestion: {
      status: 'pending' | 'running' | 'complete';
      progress: number;
    };
  };
  error?: string;                   // Error message if failed
}
```

---

## Job Lifecycle

### 1. Job Submission (`addJob()`)

**API Call**: `POST /api/pipeline/process`

**Process**:
```typescript
export async function addJob(jobData: DocumentJobData): Promise<string> {
  // 1. Validate Python environment
  await validatePythonPath();

  // 2. Generate unique job ID
  const jobId = uuidv4();

  // 3. Create initial job status
  const initialStatus: JobStatus = {
    jobId,
    fileName: jobData.fileName,
    status: 'queued',
    progress: 0,
    message: 'Queued for processing',
    createdAt: new Date().toISOString(),
    steps: {
      classification: { status: 'pending', progress: 0 },
      ner: { status: 'pending', progress: 0 },
      ingestion: { status: 'pending', progress: 0 }
    }
  };

  // 4. Store in jobStore Map
  jobStore.set(jobId, initialStatus);

  // 5. Add to processing queue
  jobQueue.push({ ...jobData, jobId });

  // 6. Trigger processing if not already running
  if (!isProcessing) {
    processQueue();
  }

  return jobId;
}
```

**Example Job Creation**:
```
Input: { files: [file1.pdf], customer: "mckenney", tags: [], classification: { sector: "Infrastructure" } }
Output: { jobId: "550e8400-e29b-41d4-a716-446655440000", status: "queued", progress: 0 }
```

---

### 2. Serial Processing (`processQueue()`)

**Algorithm**:
```typescript
async function processQueue(): Promise<void> {
  if (isProcessing) return;  // Prevent concurrent processing

  isProcessing = true;

  while (jobQueue.length > 0) {
    // 1. Get next job from queue (FIFO)
    const job = jobQueue.shift()!;

    console.log(`[Queue] Processing job ${job.jobId} (${jobQueue.length} remaining)`);

    try {
      // 2. Execute 3-stage processing pipeline
      await processDocumentJob(job);

      console.log(`[Queue] Completed job ${job.jobId}`);
    } catch (error) {
      console.error(`[Queue] Failed job ${job.jobId}:`, error);
      // Job status already updated to 'failed' in processDocumentJob
    }
  }

  isProcessing = false;
  console.log('[Queue] Queue empty, processor idle');
}
```

**Key Properties**:
- **Serial Execution**: Only ONE job processes at a time
- **FIFO Order**: Jobs process in order submitted
- **Lock Mechanism**: `isProcessing` flag prevents concurrent runs
- **Continuous Loop**: Processes until queue empty

**Example Timeline**:
```
T+0s:   Job A submitted → jobQueue = [A], processQueue() starts
T+0s:   Job B submitted → jobQueue = [A, B]
T+0s:   Job C submitted → jobQueue = [A, B, C]
T+0-15s: Job A processes (classifier → NER → ingestion)
T+15s:  Job A complete → jobQueue = [B, C]
T+15-30s: Job B processes
T+30s:  Job B complete → jobQueue = [C]
T+30-45s: Job C processes
T+45s:  Job C complete → jobQueue = []
T+45s:  isProcessing = false (idle)
```

---

### 3. Three-Stage Processing (`processDocumentJob()`)

#### Stage 1: Classification (10% → 40%)

**Purpose**: Document type classification, content analysis, sector validation

**Agent**: `agents/classifier_agent.py`

**Execution**:
```typescript
// Update status
updateJobStatus(jobId, 'classifying', 10, 'Starting document classification');

// Run Python agent
await runPythonAgent('classifier_agent.py', {
  file_path: filePath,
  sector: classification.sector,
  subsector: classification.subsector
});

// Mark complete
updateJobStatus(jobId, 'extracting', 40, 'Classification complete, starting entity extraction');
```

**Agent Arguments**:
```json
{
  "file_path": "uploads/2025-11-11_10-30-00_technical_spec.pdf",
  "sector": "Infrastructure",
  "subsector": "Water"
}
```

**Expected Output**: Classification results, document metadata, content structure

---

#### Stage 2: NER/Entity Extraction (40% → 70%)

**Purpose**: Named entity recognition, relationship identification

**Agent**: `agents/ner_agent.py`

**Execution**:
```typescript
// Already at 40% from classification
// Run NER agent
await runPythonAgent('ner_agent.py', {
  file_path: filePath,
  customer: customer
});

// Mark complete
updateJobStatus(jobId, 'ingesting', 70, 'Entity extraction complete, starting ingestion');
```

**Agent Arguments**:
```json
{
  "file_path": "uploads/2025-11-11_10-30-00_technical_spec.pdf",
  "customer": "mckenney"
}
```

**Expected Output**:
```json
{
  "entities": [
    { "text": "Siemens S7-1500", "label": "VENDOR", "confidence": 0.95, "source": "pattern" },
    { "text": "Modbus TCP", "label": "PROTOCOL", "confidence": 0.96, "source": "pattern" }
  ],
  "entity_count": 45,
  "by_type": {
    "VENDOR": 12,
    "PROTOCOL": 8,
    "STANDARD": 5
  }
}
```

---

#### Stage 3: Neo4j Ingestion (70% → 100%)

**Purpose**: Store entities and relationships in Neo4j knowledge graph

**Agent**: `agents/ingestion_agent.py`

**Execution**:
```typescript
// Already at 70% from NER
// Run ingestion agent
await runPythonAgent('ingestion_agent.py', {
  file_path: filePath,
  customer: customer,
  tags: tags,
  classification: classification
});

// Mark complete
updateJobStatus(jobId, 'complete', 100, 'Processing complete');
```

**Agent Arguments**:
```json
{
  "file_path": "uploads/2025-11-11_10-30-00_technical_spec.pdf",
  "customer": "mckenney",
  "tags": ["tag-critical", "tag-technical"],
  "classification": {
    "sector": "Infrastructure",
    "subsector": "Water"
  }
}
```

**Neo4j Operations**:
1. Create Document node with content
2. Merge Metadata node with SHA256 deduplication
3. Create Entity nodes with (text, label) composite key
4. Create CONTAINS_ENTITY relationships with confidence scores
5. Create HAS_TAG relationships for metadata tags
6. Update graph indexes and constraints

---

## Python Agent Execution

### Agent Invocation (`runPythonAgent()`)

**Implementation**:
```typescript
async function runPythonAgent(
  scriptName: string,
  args: any
): Promise<void> {
  return new Promise((resolve, reject) => {
    const pythonPath = process.env.PYTHON_PATH || 'python3';
    const agentsPath = process.env.AGENTS_PATH || path.join(__dirname, '..', '..', 'agents');
    const scriptPath = path.join(agentsPath, scriptName);

    // Spawn Python process with JSON arguments
    const pythonProcess = spawn(pythonPath, [
      scriptPath,
      JSON.stringify(args)
    ]);

    // Capture stdout
    pythonProcess.stdout.on('data', (data) => {
      console.log(`[${scriptName}] ${data}`);
    });

    // Capture stderr
    pythonProcess.stderr.on('data', (data) => {
      console.error(`[${scriptName}] ${data}`);
    });

    // Handle completion
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`${scriptName} exited with code ${code}`));
      }
    });

    // 5-minute timeout
    const timeout = setTimeout(() => {
      pythonProcess.kill('SIGTERM');
      reject(new Error(`${scriptName} timed out after 5 minutes`));
    }, 5 * 60 * 1000);

    pythonProcess.on('close', () => clearTimeout(timeout));
  });
}
```

### Environment Configuration

**Required Environment Variables** (`.env.local`):
```bash
PYTHON_PATH=python3
AGENTS_PATH=/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/agents

# Neo4j connection (used by ingestion agent)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

### Agent File Locations
```
agents/
  ├── classifier_agent.py      # Stage 1: Document classification
  ├── ner_agent.py             # Stage 2: Entity extraction
  └── ingestion_agent.py       # Stage 3: Neo4j storage
```

### Timeout Handling
- **Per-Agent Timeout**: 5 minutes
- **Action on Timeout**: Kill process with SIGTERM, mark job as failed
- **Total Pipeline Timeout**: 15 minutes maximum (3 agents × 5 min)

---

## Progress Tracking

### Progress Mapping
```
Job Progress → Agent Stage:
0%   → 'queued'      → All agents pending
10%  → 'classifying' → Agent 1 started
40%  → 'extracting'  → Agent 1 complete, Agent 2 started
70%  → 'ingesting'   → Agent 2 complete, Agent 3 started
100% → 'complete'    → All agents complete
```

### Step Progress Calculation
```typescript
function updateJobStatus(
  jobId: string,
  status: JobStatus['status'],
  progress: number,
  message: string,
  error?: string
): void {
  const job = jobStore.get(jobId);
  if (!job) return;

  // Calculate step progress based on overall progress
  const updatedJob: JobStatus = {
    ...job,
    status,
    progress,
    message,
    error,
    steps: {
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
    }
  };

  // Add completion timestamp
  if (status === 'complete' || status === 'failed') {
    updatedJob.completedAt = new Date().toISOString();
  }

  jobStore.set(jobId, updatedJob);
  console.log(`[Job ${jobId}] ${status} - ${progress}% - ${message}`);
}
```

---

## Status Retrieval

### Endpoint: `GET /api/pipeline/status/[jobId]`

**Request**:
```
GET /api/pipeline/status/550e8400-e29b-41d4-a716-446655440000
```

**Response**:
```json
{
  "success": true,
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "fileName": "technical_spec.pdf",
  "status": "extracting",
  "progress": 55,
  "message": "Extracting entities from document",
  "createdAt": "2025-11-11T10:30:00Z",
  "completedAt": null,
  "steps": {
    "classification": {
      "status": "complete",
      "progress": 100
    },
    "ner": {
      "status": "running",
      "progress": 50
    },
    "ingestion": {
      "status": "pending",
      "progress": 0
    }
  }
}
```

### Queue Status: `GET /api/pipeline/process`

**Request**:
```
GET /api/pipeline/process
```

**Response**:
```json
{
  "success": true,
  "jobs": [],
  "queueStatus": {
    "waiting": 3,      // Jobs in jobQueue
    "active": 1,       // isProcessing ? 1 : 0
    "completed": 15,   // count(status === 'complete')
    "failed": 2,       // count(status === 'failed')
    "delayed": 0,      // Always 0 (not implemented)
    "total": 21        // Sum of all
  }
}
```

---

## Error Handling

### Agent Failure Scenarios

#### Classification Failure
```
Error: classifier_agent.py crashed or timed out
Action: Job marked as 'failed', error captured
Recovery: User can retry from upload wizard
Impact: No data written to Neo4j
```

#### NER Failure
```
Error: ner_agent.py timeout (5 minutes)
Action: Job marked as 'failed'
Recovery: User can retry processing
Impact: Classification ran but results not stored
```

#### Ingestion Failure
```
Error: Neo4j connection refused
Action: Job marked as 'failed'
Recovery: Check Neo4j status, retry job
Impact: Entities extracted but not stored in graph
```

### Error Response Format
```typescript
{
  status: 'failed',
  progress: 0,
  message: 'Processing failed: [error details]',
  error: 'Full error stack trace',
  completedAt: '2025-11-11T10:35:00Z'
}
```

---

## Known Limitations

| Limitation | Impact | Production Solution |
|-----------|--------|---------------------|
| In-memory storage | Jobs lost on server restart | Use Redis-backed persistent queue (BullMQ) |
| Serial processing | Only 1 file at a time, slow for batches | Implement worker pool with parallel processing |
| No job persistence | Cannot resume after crash | Store job state in database (PostgreSQL/MongoDB) |
| 5-min timeout | Long documents may fail | Increase timeout or chunk processing |
| No retry mechanism | Transient failures cause complete failure | Implement exponential backoff retry |
| No job cancellation | Jobs run to completion | Add signal handling for graceful shutdown |
| No priority queue | All jobs equal priority | Implement priority-based scheduling |
| No dead letter queue | Failed jobs lost | Create failed job archive for debugging |
| Rate limit in-memory | Resets per server instance | Use distributed cache (Redis) |
| No job history | Can't audit past jobs | Add database audit trail |

---

## Performance Characteristics

### Processing Times (Estimated)

| Stage | Duration | Timeout |
|-------|----------|---------|
| Classification | 5-10 seconds | 5 minutes |
| NER Extraction | 10-20 seconds | 5 minutes |
| Neo4j Ingestion | 5-10 seconds | 5 minutes |
| **Total per document** | **20-40 seconds** | **15 minutes** |

### Throughput Analysis

**Serial Processing**:
- **1 document**: ~30 seconds
- **5 documents**: ~2.5 minutes (5 × 30s)
- **10 documents**: ~5 minutes (10 × 30s)
- **100 documents**: ~50 minutes (100 × 30s)

**Production Parallel Processing (5 workers)**:
- **100 documents**: ~10 minutes (100 ÷ 5 = 20 docs/worker × 30s)
- **1000 documents**: ~100 minutes (~1.67 hours)

---

## Migration Path to Production Architecture

### Recommended Upgrades

#### 1. Replace In-Memory Queue with Redis (BullMQ)
```typescript
import { Queue, Worker } from 'bullmq';

const documentQueue = new Queue('document-processing', {
  connection: {
    host: 'localhost',
    port: 6379
  }
});

const worker = new Worker('document-processing', async (job) => {
  await processDocumentJob(job.data);
}, {
  connection: { host: 'localhost', port: 6379 },
  concurrency: 5  // Process 5 jobs in parallel
});
```

#### 2. Implement Worker Pool
- **5-10 workers** for parallel processing
- **Separate queues** per agent type (classification, NER, ingestion)
- **Job dependencies** to ensure correct ordering

#### 3. Add Job Persistence
- **PostgreSQL** or **MongoDB** for job history
- **Audit trail** for compliance
- **Resume capability** after crashes

#### 4. Implement Retry Logic
```typescript
{
  attempts: 3,
  backoff: {
    type: 'exponential',
    delay: 2000  // Start with 2 seconds
  }
}
```

#### 5. Add Dead Letter Queue
```typescript
worker.on('failed', async (job, error) => {
  await deadLetterQueue.add({
    originalJob: job.data,
    error: error.message,
    failedAt: new Date()
  });
});
```

---

## Monitoring and Observability

### Current Logging
```
Console logs only:
[Queue] Processing job 550e8400-e29b-41d4-a716-446655440000 (2 remaining)
[classifier_agent.py] Starting classification...
[ner_agent.py] Extracted 45 entities
[ingestion_agent.py] Created 45 entity nodes in Neo4j
[Queue] Completed job 550e8400-e29b-41d4-a716-446655440000
```

### Production Monitoring (Recommended)
- **Prometheus** metrics for job throughput, latency, errors
- **Grafana** dashboards for real-time monitoring
- **Sentry** for error tracking and alerting
- **BullBoard** for queue visualization (if using BullMQ)

---

**DOCUMENTATION COMPLETE**
*ETL Pipeline: In-Memory Serial Processing with 3 Python Agents*
