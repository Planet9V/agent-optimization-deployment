# Five-Step User Interaction Pipeline

**File**: 02_FIVE_STEP_PIPELINE.md
**Created**: 2025-11-11
**Modified**: 2025-11-11
**Version**: 1.0.0
**Purpose**: User workflow for document upload and processing in the AEON DT AI Project
**Status**: ACTIVE

## Executive Summary

The document upload workflow is a 5-step wizard interface that guides users through uploading files, assigning metadata, and submitting documents for automated processing. The system handles document classification, entity extraction via NER v9, and ingestion into Neo4j knowledge graph.

**User Journey**: Upload Files → Assign Customer → Add Tags → Classify by Sector → Submit for Processing

**Processing Time**: ~15-30 seconds per document (3 agents × 5 min timeout each)

**Supported Formats**: PDF, DOC, DOCX, TXT, MD, XLS, XLSX, CSV

---

## Pipeline Architecture

### Workflow Overview
```
┌─────────────────────────────────────────────────────────────────┐
│           5-Step User Interaction Wizard                         │
└─────────────────────────────────────────────────────────────────┘

Step 1: UPLOAD          → Upload files to MinIO storage
   ↓
Step 2: CUSTOMER        → Assign to customer organization
   ↓
Step 3: TAGS            → Add metadata tags (optional)
   ↓
Step 4: CLASSIFY        → Select sector/subsector classification
   ↓
Step 5: PROCESS         → Submit to processing pipeline
   ↓
   ┌─────────────────────────────────────────────────┐
   │     Backend Processing (Serial Queue)           │
   ├─────────────────────────────────────────────────┤
   │ 1. Classification Agent   (10-40% progress)     │
   │ 2. NER Agent             (40-70% progress)     │
   │ 3. Ingestion Agent       (70-100% progress)    │
   └─────────────────────────────────────────────────┘
   ↓
Neo4j Knowledge Graph + Entity Relationships
```

---

## Step 1: Document Upload

### Page Location
**Component**: `/web_interface/app/upload/page.tsx`
**Wizard Component**: `/web_interface/components/upload/UploadWizard.tsx`

### User Interface
```
┌─────────────────────────────────────────────────┐
│ Step 1 of 5: Upload Documents                   │
├─────────────────────────────────────────────────┤
│                                                  │
│  [Drag & Drop Area or Click to Browse]          │
│                                                  │
│  Supported formats: PDF, DOC, DOCX, TXT, MD,    │
│                    XLS, XLSX, CSV                │
│  Maximum file size: 100 MB per file             │
│  Maximum files: 20 files per upload             │
│                                                  │
│  [Uploaded Files List]                          │
│  ✓ document1.pdf (2.5 MB)                       │
│  ✓ document2.docx (1.3 MB)                      │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Supported Formats
| Format | Extension | MIME Type | Max Size |
|--------|-----------|-----------|----------|
| PDF | `.pdf` | `application/pdf` | 100 MB |
| Word | `.doc`, `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | 100 MB |
| Text | `.txt`, `.md` | `text/plain`, `text/markdown` | 100 MB |
| Excel | `.xls`, `.xlsx` | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | 100 MB |
| CSV | `.csv` | `text/csv` | 100 MB |

### Upload API Endpoint
**Endpoint**: `POST /api/upload`
**Handler**: `/web_interface/app/api/upload/route.ts`

**Request**:
```typescript
FormData {
  files: File[]  // Multiple files in single upload
}
```

**Response**:
```json
{
  "success": true,
  "files": [
    {
      "originalName": "technical_spec.pdf",
      "path": "uploads/2025-11-11_10-30-00_technical_spec.pdf",
      "bucket": "aeon-documents",
      "size": 1024000,
      "type": "application/pdf",
      "metadata": {
        "uploadedAt": "2025-11-11T10:30:00Z",
        "sha256": "abc123..."
      }
    }
  ],
  "count": 1
}
```

### File Storage (MinIO)
**Configuration** (`.env.local`):
```bash
MINIO_ENDPOINT=openspg-minio
MINIO_PORT=9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_USE_SSL=false
MINIO_BUCKET=aeon-documents
```

**Path Format**: `uploads/YYYY-MM-DD_HH-MM-SS_filename.ext`

**Example Paths**:
- `uploads/2025-11-11_10-30-00_technical_spec.pdf`
- `uploads/2025-11-11_10-31-15_security_audit.docx`

### Validation Rules
| Rule | Enforcement | Error Message |
|------|------------|--------------|
| File size ≤ 100 MB | Frontend + Backend | "File exceeds maximum size of 100MB" |
| Max 20 files per upload | Frontend | "Maximum 20 files allowed" |
| Supported formats only | Frontend | "Unsupported file format" |
| No empty files | Backend | "File is empty" |

### Progress Indicator
```
Upload Files
[████████████████████████████] 100%
✓ 2 files uploaded successfully
```

---

## Step 2: Customer Assignment

### User Interface
```
┌─────────────────────────────────────────────────┐
│ Step 2 of 5: Assign to Customer                 │
├─────────────────────────────────────────────────┤
│                                                  │
│  Customer: [Dropdown▼]                          │
│  ┌─────────────────────────────────────┐        │
│  │ McKenney's Inc. (Primary)          │        │
│  │ Demo Corporation (Demo)             │        │
│  │ Test Client (Test)                  │        │
│  └─────────────────────────────────────┘        │
│                                                  │
│  Selected Customer:                             │
│  ┌─────────────────────────────────────┐        │
│  │ McKenney's Inc.                     │        │
│  └─────────────────────────────────────┘        │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Available Customers
```typescript
const CUSTOMERS = [
  { id: 'mckenney', name: 'McKenney\'s Inc.', type: 'Primary' },
  { id: 'demo-corp', name: 'Demo Corporation', type: 'Demo' },
  { id: 'test-client', name: 'Test Client', type: 'Test' }
];
```

### Purpose
- **Document Ownership**: Associate documents with customer organization
- **Multi-tenancy**: Separate document collections by customer
- **Access Control**: Future customer-based permissions
- **Metadata**: Customer context for Neo4j storage

### Validation
- **Required Field**: Cannot proceed to Step 3 without customer selection
- **Frontend Check**: `selectedCustomer !== ''`

---

## Step 3: Metadata Tags (Optional)

### User Interface
```
┌─────────────────────────────────────────────────┐
│ Step 3 of 5: Add Metadata Tags                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  Select tags to categorize documents (optional) │
│                                                  │
│  [🔴 Critical] [🟠 Confidential] [🟡 Internal] │
│  [🟢 Public]   [🔵 Technical]    [🟣 Compliance]│
│  [🟣 Architectural] [🩷 Audit]                  │
│                                                  │
│  Selected Tags (3/5):                           │
│  [🔴 Critical ×] [🔵 Technical ×] [🟣 Compliance ×] │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Available Tags
```typescript
const AVAILABLE_TAGS = [
  { id: 'tag-critical', name: 'Critical', color: 'red' },
  { id: 'tag-confidential', name: 'Confidential', color: 'orange' },
  { id: 'tag-internal', name: 'Internal', color: 'yellow' },
  { id: 'tag-public', name: 'Public', color: 'green' },
  { id: 'tag-technical', name: 'Technical', color: 'blue' },
  { id: 'tag-architectural', name: 'Architectural', color: 'indigo' },
  { id: 'tag-compliance', name: 'Compliance', color: 'purple' },
  { id: 'tag-audit', name: 'Audit', color: 'pink' }
];
```

### Tag Functionality
- **Multiple Selection**: Users can select 0-5 tags
- **Visual Indicators**: Color-coded badges for easy identification
- **Optional**: Can proceed to Step 4 without tags
- **Neo4j Storage**: Tags stored as relationships to Document nodes

### Tag Component
**Component**: `/web_interface/components/tags/TagSelector.tsx`

**Props**:
```typescript
interface TagSelectorProps {
  availableTags: Tag[];
  selectedTags: string[];
  onTagsChange: (tags: string[]) => void;
  allowCreate?: boolean;
  maxTags?: number;
}
```

---

## Step 4: Document Classification

### User Interface
```
┌─────────────────────────────────────────────────┐
│ Step 4 of 5: Document Classification            │
├─────────────────────────────────────────────────┤
│                                                  │
│  Sector: * [Dropdown▼]                          │
│  ┌─────────────────────────────────────┐        │
│  │ Infrastructure                      │        │
│  │ Industrial Controls                 │        │
│  │ Healthcare                           │        │
│  │ Energy                               │        │
│  │ Financial                            │        │
│  │ Government                           │        │
│  │ Education                            │        │
│  │ Telecommunications                   │        │
│  └─────────────────────────────────────┘        │
│                                                  │
│  Subsector: [Dropdown▼]                         │
│  ┌─────────────────────────────────────┐        │
│  │ Water                                │        │
│  │ Transportation                       │        │
│  │ Power Grid                           │        │
│  └─────────────────────────────────────┘        │
│                                                  │
│  Classification:                                │
│  ┌─────────────────────────────────────┐        │
│  │ Sector: Infrastructure → Water      │        │
│  └─────────────────────────────────────┘        │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Sector Options
```typescript
const SECTORS = [
  'Infrastructure',
  'Industrial Controls',
  'Healthcare',
  'Energy',
  'Financial',
  'Government',
  'Education',
  'Telecommunications'
];
```

### Subsector Mapping
```typescript
const SUBSECTORS = {
  Infrastructure: ['Water', 'Transportation', 'Power Grid'],
  'Industrial Controls': ['SCADA', 'PLC', 'DCS', 'HMI'],
  Healthcare: ['Medical Devices', 'Patient Data', 'Lab Systems'],
  Energy: ['Oil & Gas', 'Nuclear', 'Renewable'],
  Financial: ['Banking', 'Trading', 'Payment Systems'],
  Government: ['Federal', 'State', 'Local', 'Military'],
  Education: ['K-12', 'Higher Education', 'Research'],
  Telecommunications: ['Mobile', 'Broadband', '5G']
};
```

### Classification Purpose
- **Document Context**: Industry sector for classification agent
- **Entity Filtering**: Domain-specific NER patterns
- **Graph Organization**: Sector-based document grouping
- **Search Facets**: Filter documents by industry

### Validation
- **Sector Required**: Cannot proceed without sector selection
- **Subsector Optional**: Subsector dropdown only appears if sector selected
- **Dynamic Options**: Subsector options change based on sector

---

## Step 5: Submit for Processing

### User Interface - Summary
```
┌─────────────────────────────────────────────────┐
│ Step 5 of 5: Submit for Processing              │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌───────────────────────────────────┐          │
│  │ Files: 2 documents                │          │
│  └───────────────────────────────────┘          │
│                                                  │
│  ┌───────────────────────────────────┐          │
│  │ Customer: McKenney's Inc.         │          │
│  └───────────────────────────────────┘          │
│                                                  │
│  ┌───────────────────────────────────┐          │
│  │ Tags: [Critical] [Technical]      │          │
│  └───────────────────────────────────┘          │
│                                                  │
│  ┌───────────────────────────────────┐          │
│  │ Classification:                   │          │
│  │ Infrastructure → Water            │          │
│  └───────────────────────────────────┘          │
│                                                  │
│  [Start Processing ⚡]                          │
│                                                  │
└─────────────────────────────────────────────────┘
```

### User Interface - Processing Status
```
┌─────────────────────────────────────────────────┐
│ Processing Status                                │
├─────────────────────────────────────────────────┤
│                                                  │
│ technical_spec.pdf                              │
│ Classification complete, starting extraction    │
│ [██████████████████░░░░░░░░] 45%     extracting│
│                                                  │
│ security_audit.docx                             │
│ Queued for processing                           │
│ [░░░░░░░░░░░░░░░░░░░░░░░░░] 0%        queued   │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Submit API Endpoint
**Endpoint**: `POST /api/pipeline/process`
**Handler**: `/web_interface/app/api/pipeline/process/route.ts`

**Request Body**:
```typescript
{
  files: [
    {
      path: "uploads/2025-11-11_10-30-00_technical_spec.pdf",
      name: "technical_spec.pdf",
      size: 1024000,
      type: "application/pdf"
    }
  ],
  customer: "mckenney",
  tags: ["tag-critical", "tag-technical"],
  classification: {
    sector: "Infrastructure",
    subsector: "Water"
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
      "message": "Queued: technical_spec.pdf",
      "fileName": "technical_spec.pdf"
    }
  ],
  "message": "Started processing 1 file(s)"
}
```

### Real-Time Progress Polling
**Endpoint**: `GET /api/pipeline/status/[jobId]`
**Polling Interval**: 2 seconds

**Response During Processing**:
```json
{
  "success": true,
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "fileName": "technical_spec.pdf",
  "status": "extracting",
  "progress": 45,
  "message": "Classification complete, starting entity extraction",
  "createdAt": "2025-11-11T10:30:00Z",
  "steps": {
    "classification": { "status": "complete", "progress": 100 },
    "ner": { "status": "running", "progress": 50 },
    "ingestion": { "status": "pending", "progress": 0 }
  }
}
```

### Processing Stages
```
Progress Mapping:
0%   → status: 'queued'     → All steps pending
10%  → status: 'classifying' → Classification agent running
40%  → status: 'extracting' → NER agent running
70%  → status: 'ingesting'  → Ingestion agent running
100% → status: 'complete'   → All processing complete
```

### Completion Screen
```
┌─────────────────────────────────────────────────┐
│           ✓ Processing Complete!                │
├─────────────────────────────────────────────────┤
│                                                  │
│  All documents have been processed successfully │
│  and ingested into the knowledge graph.         │
│                                                  │
│  [Upload More Documents]                        │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## User Experience Flow

### Happy Path Timeline
```
T+0s:    User lands on upload page
T+5s:    User uploads 2 PDF files
T+10s:   User selects customer "McKenney's Inc."
T+15s:   User adds tags [Critical, Technical]
T+20s:   User selects "Infrastructure → Water"
T+25s:   User clicks "Start Processing"
         ↓
         Backend creates 2 jobs in queue
         ↓
T+25-40s: Job 1 processes (classifier → NER → ingestion)
T+40-55s: Job 2 processes (classifier → NER → ingestion)
         ↓
T+55s:   Processing complete, success screen shown
         User clicks "Upload More Documents"
         Wizard resets to Step 1
```

### Error Scenarios

#### Upload Failure
```
Error: File too large (150 MB)
Action: Show error message, prevent upload
Recovery: User removes large file, uploads smaller files
```

#### Processing Failure
```
Error: NER agent timeout (5 minutes exceeded)
Status: Job marked as 'failed', error message shown
Recovery: User can view error details, retry processing
```

#### Network Interruption
```
Error: Polling interrupted, cannot fetch job status
Action: Show warning "Connection lost, retrying..."
Recovery: Automatic reconnection, resume polling
```

### Performance Expectations

| Operation | Expected Time | Timeout |
|-----------|--------------|---------|
| File upload to MinIO | 1-5 seconds per file | 30 seconds |
| Job submission | <500ms | 5 seconds |
| Classification agent | 5-10 seconds | 5 minutes |
| NER agent | 10-20 seconds | 5 minutes |
| Ingestion agent | 5-10 seconds | 5 minutes |
| **Total per document** | **20-40 seconds** | **15 minutes** |

**Serial Processing Note**: Only 1 document processes at a time. If 5 documents uploaded, total time = 5 × 30 seconds = 2.5 minutes.

---

## Integration with Backend

### API Endpoints Summary

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/api/upload` | POST | Upload files to MinIO | Required (Clerk) |
| `/api/pipeline/process` | POST | Submit job to queue | Required (Clerk) |
| `/api/pipeline/status/[jobId]` | GET | Get job status | None (should be added) |
| `/api/pipeline/process` | GET | Get queue status | None |

### State Management (React)

**Component State**:
```typescript
const [currentStep, setCurrentStep] = useState<number>(1);
const [uploadedFiles, setUploadedFiles] = useState<UploadedFileInfo[]>([]);
const [selectedCustomer, setSelectedCustomer] = useState<string>('');
const [selectedTags, setSelectedTags] = useState<string[]>([]);
const [selectedSector, setSelectedSector] = useState<string>('');
const [selectedSubsector, setSelectedSubsector] = useState<string>('');
const [isProcessing, setIsProcessing] = useState<boolean>(false);
const [processingJobs, setProcessingJobs] = useState<ProcessingJob[]>([]);
const [isComplete, setIsComplete] = useState<boolean>(false);
```

### Navigation Logic
```typescript
// Step validation
const canProceedToNext = () => {
  switch (currentStep) {
    case 1: return uploadedFiles.length > 0;
    case 2: return selectedCustomer !== '';
    case 3: return true; // Tags optional
    case 4: return selectedSector !== '';
    case 5: return false; // Final step
  }
};

// Next button handler
const handleNext = () => {
  if (currentStep < 5 && canProceedToNext()) {
    setCurrentStep(currentStep + 1);
  }
};
```

### Progress Bar Calculation
```typescript
const progressPercentage = (currentStep / STEPS.length) * 100;
// Step 1/5 = 20%, Step 2/5 = 40%, Step 3/5 = 60%, etc.
```

---

## Key Features

### Visual Progress Indicators
- **Step Icons**: Upload, Building, Tag, FileType, Zap icons
- **Checkmarks**: Green checkmarks for completed steps
- **Color Coding**: Blue (active), Green (complete), Gray (pending)
- **Progress Bar**: Percentage completion across top of wizard

### Data Validation
- **Required Fields**: Customer, Sector (cannot proceed without)
- **Optional Fields**: Tags, Subsector (can skip)
- **File Size**: 100 MB per file hard limit
- **Max Files**: 20 files per batch upload

### User Feedback
- **Success Messages**: Green banners for successful uploads
- **Error Messages**: Red alerts for failures
- **Loading States**: Spinner on "Start Processing" button
- **Real-time Updates**: Progress bars update every 2 seconds

---

**DOCUMENTATION COMPLETE**
*Five-Step Pipeline: Upload → Customer → Tags → Classify → Process*
