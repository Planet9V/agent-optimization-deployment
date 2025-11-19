# Pipeline API - Quick Reference

## 3-Minute Overview

The pipeline is a **serial document processing system** that:
1. Accepts file uploads via `/api/pipeline/process` (POST)
2. Queues them for processing in FIFO order
3. Processes each job through 3 stages: Classification → NER → Ingestion
4. Returns job status via `/api/pipeline/status/[jobId]` (GET)

---

## API Endpoints

### Submit Job: POST `/api/pipeline/process`
```bash
curl -X POST https://api.example.com/api/pipeline/process \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      {
        "path": "/uploads/document.pdf",
        "name": "document.pdf",
        "size": 1024000,
        "type": "application/pdf"
      }
    ],
    "customer": "acme-corp",
    "tags": ["critical", "healthcare"],
    "classification": {
      "sector": "healthcare",
      "subsector": "medical-devices"
    }
  }'

# Response
{
  "success": true,
  "jobs": [{
    "jobId": "550e8400-e29b-41d4-a716-446655440000",
    "status": "queued",
    "progress": 0
  }],
  "message": "Started processing 1 file(s)"
}
```

### Get Job Status: GET `/api/pipeline/status/[jobId]`
```bash
curl https://api.example.com/api/pipeline/status/550e8400-e29b-41d4-a716-446655440000

# Response
{
  "success": true,
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "fileName": "document.pdf",
  "status": "extracting",
  "progress": 50,
  "message": "Classification complete, starting entity extraction",
  "steps": {
    "classification": { "status": "complete", "progress": 100 },
    "ner": { "status": "running", "progress": 50 },
    "ingestion": { "status": "pending", "progress": 0 }
  }
}
```

### Get Queue Status: GET `/api/pipeline/process`
```bash
curl https://api.example.com/api/pipeline/process

# Response
{
  "success": true,
  "queueStatus": {
    "waiting": 3,
    "active": 1,
    "completed": 15,
    "failed": 0,
    "total": 19
  }
}
```

---

## Processing Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                   Document Processing Flow                   │
└─────────────────────────────────────────────────────────────┘

CLIENT                    API                         AGENTS
  │                        │                           │
  ├─ POST /process ────────>│                          │
  │                        ├─ Validation              │
  │                        ├─ Create Job              │
  │                        ├─ Add to Queue            │
  │                    <───┤ Response (queued)        │
  │                        │                          │
  │                        ├─ Start processQueue()    │
  │                        ├─ Extract job from queue  │
  │                        ├─ Call runPythonAgent()   │
  │                        │                   ┌──────>│
  │                        │          Stage 1: classifier_agent.py
  │  (polling)             │          (0-5 min, progress: 10→40%)
  ├─ GET /status/jobId ───>│          (output: classification)
  │                    <───┤          
  │  Result: 10% progress  │                   <──────┤
  │                        │                          │
  │  (polling)             │                          │
  ├─ GET /status/jobId ───>│          ┌──────>│
  │                    <───┤          │ Stage 2: ner_agent.py
  │  Result: 40% progress  │          │ (0-5 min, progress: 40→70%)
  │                        │          │ (output: entities & relationships)
  │  (polling)             │          │
  ├─ GET /status/jobId ───>│          <──────┤
  │                    <───┤                  │
  │  Result: 70% progress  │          ┌──────>│
  │                        │          │ Stage 3: ingestion_agent.py
  │                        │          │ (0-5 min, progress: 70→100%)
  │  (polling)             │          │ (output: Neo4j graph updated)
  ├─ GET /status/jobId ───>│          │
  │                    <───┤          <──────┤
  │  Result: 100% complete │                 │
  │
```

---

## Key Concepts

### Job States
```
queued      → Waiting in queue (progress: 0%)
classifying → Running classifier_agent.py (progress: 10-40%)
extracting  → Running ner_agent.py (progress: 40-70%)
ingesting   → Running ingestion_agent.py (progress: 70-100%)
complete    → Finished successfully (progress: 100%)
failed      → Error during processing (progress: 0%, error set)
```

### Processing Characteristics
- **Serial**: Only one job processes at a time (FIFO queue)
- **Timeout**: Each stage has 5-minute timeout
- **Atomic**: Stages run sequentially; failure at any stage fails entire job
- **In-Memory**: All state lost on server restart
- **Authentication**: POST requires Clerk auth; GET status route does NOT

---

## NER (Named Entity Recognition) Integration

### When Invoked
**Stage 2** of the processing pipeline, after successful classification

### Python Agent
```
Script: ner_agent.py
Input Args:
  - file_path: Path to document
  - customer: Customer identifier
Output: Entities and relationships written to temp storage
```

### Progress
- **Start**: 40% (when classification completes)
- **End**: 70% (when entity extraction completes)
- **Timeout**: 5 minutes

### Data Flow
```
Document File
    ↓
[classifier_agent.py runs]
    ↓
Classification Results (stored)
    ↓
[ner_agent.py runs] ← **NER v9 invoked here**
    ↓
Entities: { name, type, confidence, location }
Relationships: { entity1, type, entity2 }
    ↓
[ingestion_agent.py runs]
    ↓
Neo4j Graph (entities as nodes, relationships as edges)
```

---

## Error Handling

### Request-Level Errors
```
401 Unauthorized        → Add authentication
400 Bad Request        → Check required fields (customer, sector, files)
413 Payload Too Large  → File exceeds 100MB limit
429 Too Many Requests  → Rate limit (100 req/15 min per IP)
500 Server Error       → Python environment misconfigured
```

### Processing-Level Errors
```
Job Status: 'failed'
Progress: 0%
Error: (contains Python agent error message)
```

Failure cases:
- **Classification fails** → Job fails, NER/Ingestion don't run
- **NER fails** → Job fails, Ingestion doesn't run, Classification persists
- **Ingestion fails** → Job fails, Neo4j not updated, NER results may persist

---

## Configuration

| Environment Variable | Default | Purpose |
|---|---|---|
| `PYTHON_PATH` | `python3` | Python executable |
| `AGENTS_PATH` | `../agents` | Python agents directory |
| `UPLOAD_DIR` | `/uploads` | Safe directory for files |

**Validation**: Python path checked before processing starts

---

## Monitoring

### Queue Status
```json
{
  "waiting": 0,      // Jobs not yet started
  "active": 0,       // Currently processing
  "completed": 42,   // Successfully finished
  "failed": 1,       // Failed jobs
  "total": 43
}
```

### Individual Job
```json
{
  "jobId": "...",
  "status": "extracting",
  "progress": 55,
  "steps": {
    "classification": { "status": "complete", "progress": 100 },
    "ner": { "status": "running", "progress": 50 },
    "ingestion": { "status": "pending", "progress": 0 }
  }
}
```

---

## Known Issues & Limitations

1. **No persistence**: Jobs lost on server restart
2. **Serial processing**: Only 1 file at a time (bottleneck)
3. **Status route unauthenticated**: Security vulnerability
4. **5-min timeout**: Long documents may fail
5. **In-memory rate limit**: Ineffective across multiple servers
6. **No job history**: Can't audit past processing

---

## Development Notes

### Source Files
- **Route Handler**: `/app/api/pipeline/process/route.ts`
- **Status Handler**: `/app/api/pipeline/status/[jobId]/route.ts`
- **Queue Logic**: `/lib/queue/documentQueue.ts`

### Python Agent Communication
```typescript
// Arguments passed as JSON string to Python script
spawn(pythonPath, [scriptPath, JSON.stringify(args)])

// Python receives via: sys.argv[1]
import json
args = json.loads(sys.argv[1])
file_path = args['file_path']
customer = args['customer']
```

### Testing
```bash
# Submit job
curl -X POST http://localhost:3000/api/pipeline/process \
  -H "Content-Type: application/json" \
  -d '{"files":[...],"customer":"test",...}'

# Check status
curl http://localhost:3000/api/pipeline/status/[jobId]

# Monitor queue
curl http://localhost:3000/api/pipeline/process
```

---

## Next Steps for Improvement

1. ✅ Replace in-memory with Redis for persistence
2. ✅ Add parallel processing pools
3. ✅ Add authentication to status endpoint
4. ✅ Make timeout configurable per stage
5. ✅ Implement job cancellation
6. ✅ Add job history database
7. ✅ Implement distributed rate limiting
8. ✅ Add webhooks for job completion

