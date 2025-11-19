# Upload Pipeline Documentation

## Overview

The AEON Upload Pipeline is a 5-step wizard that guides users through uploading, classifying, and processing documents into the AEON Digital Twin knowledge graph system.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    5-Step Upload Wizard                      │
├─────────────────────────────────────────────────────────────┤
│ Step 1: Upload    → MinIO Object Storage                     │
│ Step 2: Customer  → Assign to Organization                   │
│ Step 3: Tags      → Add Metadata Tags                        │
│ Step 4: Classify  → Sector/Subsector Classification          │
│ Step 5: Process   → Submit to Python Processing Pipeline     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              Python Agent Processing Pipeline                │
├─────────────────────────────────────────────────────────────┤
│ 1. Classifier Agent    → Document classification             │
│ 2. NER Agent          → Named entity extraction              │
│ 3. Ingestion Agent    → Neo4j knowledge graph insertion      │
└─────────────────────────────────────────────────────────────┘
```

## File Structure

```
/app/upload/page.tsx                    - Upload page component
/components/upload/UploadWizard.tsx     - Main wizard component (5 steps)
/components/upload/FileUpload.tsx       - File upload UI component
/components/upload/UploadProgress.tsx   - Progress tracking component
/components/tags/TagSelector.tsx        - Tag selection component

/app/api/upload/route.ts                - MinIO file upload endpoint
/app/api/pipeline/process/route.ts      - Processing job creation
/app/api/pipeline/status/[jobId]/route.ts - Job status tracking
```

## 5-Step Wizard Flow

### Step 1: Upload Files

**Purpose**: Select and upload documents to MinIO object storage

**Features**:
- Drag & drop file upload
- Multi-file selection (up to 20 files)
- File validation (type, size)
- Supported formats: PDF, DOC, DOCX, TXT, MD, XLS, XLSX, CSV
- Max file size: 100MB per file
- Progress tracking

**API Endpoint**: `POST /api/upload`

**Implementation**:
```typescript
// Upload files to MinIO
const formData = new FormData();
files.forEach(file => formData.append('files', file));

const response = await fetch('/api/upload', {
  method: 'POST',
  body: formData
});

// Returns: { files: [...], count: number }
```

### Step 2: Assign Customer

**Purpose**: Link documents to a customer organization

**Options**:
- McKenney's Inc. (Primary)
- Demo Corporation (Demo)
- Test Client (Test)

**Required**: Yes

### Step 3: Add Tags (Optional)

**Purpose**: Add metadata tags for categorization

**Available Tags**:
- Critical (red)
- Confidential (orange)
- Internal (yellow)
- Public (green)
- Technical (blue)
- Architectural (indigo)
- Compliance (purple)
- Audit (pink)

**Features**:
- Multi-select (max 5 tags)
- Search functionality
- Tag creation (if enabled)

**Required**: No

### Step 4: Classification

**Purpose**: Classify documents by industry sector and subsector

**Sectors**:
- Infrastructure
- Industrial Controls
- Healthcare
- Energy
- Financial
- Government
- Education
- Telecommunications

**Subsectors**: Dynamic based on selected sector

**Required**: Yes (sector), Optional (subsector)

### Step 5: Process & Submit

**Purpose**: Review selections and submit for processing

**Summary Display**:
- Number of files
- Selected customer
- Applied tags
- Classification (sector/subsector)

**Processing Pipeline**:
1. **Classifying** (33%) - Document classification via classifier_agent.py
2. **Extracting** (66%) - Entity extraction via ner_agent.py
3. **Ingesting** (100%) - Knowledge graph insertion via ingestion_agent.py

**API Endpoint**: `POST /api/pipeline/process`

## API Endpoints

### POST /api/upload

Upload files to MinIO object storage.

**Request**:
```
Content-Type: multipart/form-data
Body: FormData with 'files' array
```

**Response**:
```json
{
  "success": true,
  "files": [
    {
      "originalName": "document.pdf",
      "path": "uploads/2025-11-03_17-30-45_document.pdf",
      "bucket": "aeon-documents",
      "size": 1024000,
      "type": "application/pdf",
      "url": "http://minio:9000/...",
      "metadata": {
        "uploadedAt": "2025-11-03T17:30:45.000Z",
        "fileName": "2025-11-03_17-30-45_document.pdf"
      }
    }
  ],
  "count": 1
}
```

### POST /api/pipeline/process

Submit files for processing through the pipeline.

**Request**:
```json
{
  "files": [
    {
      "path": "uploads/2025-11-03_17-30-45_document.pdf",
      "name": "document.pdf",
      "size": 1024000,
      "type": "application/pdf"
    }
  ],
  "customer": "mckenney",
  "tags": ["tag-critical", "tag-technical"],
  "classification": {
    "sector": "Infrastructure",
    "subsector": "Water"
  }
}
```

**Response**:
```json
{
  "success": true,
  "jobs": [
    {
      "jobId": "550e8400-e29b-41d4-a716-446655440000",
      "status": "queued",
      "progress": 0,
      "message": "Queued: document.pdf"
    }
  ],
  "message": "Started processing 1 file(s)"
}
```

### GET /api/pipeline/status/[jobId]

Get processing status for a specific job.

**Response**:
```json
{
  "success": true,
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "fileName": "document.pdf",
  "status": "classifying",
  "progress": 33,
  "message": "Classifying document...",
  "createdAt": "2025-11-03T17:30:45.000Z",
  "steps": {
    "classification": { "status": "running", "progress": 50 },
    "ner": { "status": "pending", "progress": 0 },
    "ingestion": { "status": "pending", "progress": 0 }
  },
  "customer": "mckenney",
  "tags": ["tag-critical", "tag-technical"],
  "classification": {
    "sector": "Infrastructure",
    "subsector": "Water"
  }
}
```

## Python Agent Integration

The pipeline calls Python agents in sequence:

### 1. Classifier Agent

**Script**: `agents/classifier_agent.py`

**Arguments**:
```json
{
  "file_path": "uploads/2025-11-03_17-30-45_document.pdf",
  "sector": "Infrastructure",
  "subsector": "Water"
}
```

**Responsibilities**:
- Document type classification
- Content analysis
- Sector/subsector validation

### 2. NER Agent

**Script**: `agents/ner_agent.py`

**Arguments**:
```json
{
  "file_path": "uploads/2025-11-03_17-30-45_document.pdf",
  "customer": "mckenney"
}
```

**Responsibilities**:
- Named entity extraction
- Relationship identification
- Entity classification

### 3. Ingestion Agent

**Script**: `agents/ingestion_agent.py`

**Arguments**:
```json
{
  "file_path": "uploads/2025-11-03_17-30-45_document.pdf",
  "customer": "mckenney",
  "tags": ["tag-critical", "tag-technical"],
  "classification": {
    "sector": "Infrastructure",
    "subsector": "Water"
  }
}
```

**Responsibilities**:
- Neo4j node creation
- Relationship mapping
- Property assignment
- Graph integration

## Environment Configuration

Required environment variables in `.env.local`:

```bash
# MinIO Configuration
MINIO_ENDPOINT=openspg-minio
MINIO_PORT=9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_USE_SSL=false
MINIO_BUCKET=aeon-documents

# Python Agents
PYTHON_PATH=python3
AGENTS_PATH=/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/agents
```

## Usage

### Access the Upload Pipeline

Navigate to: `http://localhost:3000/upload`

### Complete Upload Workflow

1. **Upload Files**: Drag & drop or select files
2. **Select Customer**: Choose from available organizations
3. **Add Tags**: (Optional) Add metadata tags
4. **Classify**: Select sector and subsector
5. **Process**: Review and submit for processing

### Monitor Progress

- Real-time progress updates during processing
- Step-by-step status tracking
- Error handling and retry options
- Completion notification

## Error Handling

### Upload Errors
- File validation failures
- MinIO connection issues
- File size/type restrictions

### Processing Errors
- Python agent execution failures
- Neo4j connection issues
- Data validation errors

All errors are logged and displayed to the user with actionable messages.

## Production Considerations

### Scaling

1. **Job Queue**: Implement Redis-based job queue for production
2. **Worker Processes**: Use separate worker processes for Python agents
3. **Load Balancing**: Distribute processing across multiple workers

### State Management

Current implementation uses in-memory Map for job storage. For production:

```typescript
// Replace with Redis
import { Redis } from 'ioredis';
const redis = new Redis(process.env.REDIS_URL);

// Store job
await redis.set(`job:${jobId}`, JSON.stringify(job));

// Retrieve job
const job = JSON.parse(await redis.get(`job:${jobId}`));
```

### Monitoring

- Add APM (Application Performance Monitoring)
- Log aggregation (e.g., ELK stack)
- Metrics collection (Prometheus/Grafana)
- Alert system for failures

## Testing

### Unit Tests

```bash
# Test upload API
npm test app/api/upload/route.test.ts

# Test processing pipeline
npm test app/api/pipeline/process/route.test.ts
```

### Integration Tests

```bash
# Test full upload workflow
npm test integration/upload-pipeline.test.ts
```

### E2E Tests

```bash
# Test complete user journey
npm run e2e:upload
```

## Future Enhancements

1. **Batch Upload**: Support for uploading entire directories
2. **Template Selection**: Pre-configured classification templates
3. **Auto-Classification**: ML-based automatic sector classification
4. **Progress Notifications**: Email/webhook notifications on completion
5. **File Preview**: Preview documents before processing
6. **Version Control**: Track document versions and updates
7. **Advanced Search**: Search processed documents by content
8. **Analytics Dashboard**: Processing statistics and trends

## Support

For issues or questions:
- Check logs: `/var/log/aeon-ui/`
- Review Python agent logs: `/var/log/agents/`
- Contact: AEON Development Team
