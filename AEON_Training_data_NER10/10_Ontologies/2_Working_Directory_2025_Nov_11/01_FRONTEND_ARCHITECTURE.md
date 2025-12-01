# Frontend Architecture - Next.js 15

**File**: 01_FRONTEND_ARCHITECTURE.md
**Created**: 2025-11-11 10:30:00 UTC
**Modified**: 2025-11-11 10:30:00 UTC
**Version**: 1.0.0
**Purpose**: Next.js 15 frontend architecture and implementation details for AEON DT
**Status**: ACTIVE

## Executive Summary

The AEON DT frontend is built with Next.js 15.0.3 using the App Router architecture, React 19.0.0, and TypeScript. The application provides a five-step document upload wizard, real-time job monitoring, knowledge graph visualization, and semantic search capabilities. Authentication is handled by Clerk, styling uses TailwindCSS with Tremor components for data visualization.

**Key Features**:
- Five-step upload wizard with progress tracking
- Real-time job status monitoring
- Knowledge graph visualization
- Semantic search interface
- Clerk authentication integration
- Responsive design with TailwindCSS

**Technology Stack**: Next.js 15 App Router, React 19, TypeScript 5, TailwindCSS, Tremor, Framer Motion

## Technology Stack

### Core Framework
- **Next.js**: 15.0.3 (App Router with React Server Components)
- **React**: 19.0.0
- **TypeScript**: 5+
- **Node.js**: 18+ required

### UI/Styling
- **TailwindCSS**: Utility-first CSS framework
- **Tremor**: Data visualization components (`@tremor/react` 3.18.5)
- **Radix UI**: Accessible component primitives
- **Lucide React**: Icon library
- **Framer Motion**: Animation library (11.18.0)

### State Management
- **React Server Components**: Server-side rendering and data fetching
- **Client Components**: Interactive UI with hooks
- **React Context**: Global state for user/session data

### Data Fetching
- **Server Components**: Direct database queries (Neo4j, MySQL)
- **API Routes**: REST endpoints for client-side operations
- **MinIO Client**: File upload/download operations (`minio` 8.0.2)
- **Neo4j Driver**: Graph database queries (`neo4j-driver` 5.27.0)

### Authentication
- **Clerk**: Complete authentication system (`@clerk/nextjs` 6.7.3)
- **Session Management**: Clerk-managed sessions
- **Role-Based Access**: Admin, user, viewer roles

## Application Structure

### Directory Layout

```
web_interface/
├── app/                          # Next.js 15 App Router
│   ├── (auth)/                   # Auth-protected routes
│   │   ├── dashboard/
│   │   ├── upload/
│   │   ├── documents/
│   │   ├── graph/
│   │   └── search/
│   ├── api/                      # API routes
│   │   ├── upload/               # File upload endpoint
│   │   ├── pipeline/             # Pipeline processing
│   │   │   ├── process/
│   │   │   └── status/[jobId]/
│   │   ├── health/               # Health check
│   │   └── ...
│   ├── components/               # React components
│   │   ├── upload/
│   │   │   ├── UploadWizard.tsx
│   │   │   ├── FileUpload.tsx
│   │   │   ├── ClassificationStep.tsx
│   │   │   ├── EntityConfigStep.tsx
│   │   │   ├── RelationshipConfigStep.tsx
│   │   │   └── ProcessingStep.tsx
│   │   ├── graph/
│   │   ├── search/
│   │   └── ui/                   # Shared UI components
│   ├── lib/                      # Utilities and integrations
│   │   ├── queue/
│   │   │   └── documentQueue.ts  # BullMQ queue management
│   │   ├── minio.ts              # MinIO client
│   │   ├── neo4j.ts              # Neo4j client
│   │   └── utils.ts
│   ├── types/                    # TypeScript type definitions
│   │   ├── document.ts
│   │   ├── entity.ts
│   │   └── job.ts
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Home page
├── public/                       # Static assets
├── styles/                       # Global styles
├── .env.local                    # Environment variables
├── next.config.js                # Next.js configuration
├── tailwind.config.js            # TailwindCSS configuration
├── tsconfig.json                 # TypeScript configuration
└── package.json                  # Dependencies
```

### Routing Architecture

**App Router Structure** (Next.js 15):
```
/                              # Home/Dashboard
/upload                        # Five-step upload wizard
/documents                     # Document management
/documents/[id]                # Document detail view
/graph                         # Knowledge graph visualization
/search                        # Semantic search interface
/api/upload                    # File upload API
/api/pipeline/process          # Process documents
/api/pipeline/status/[jobId]   # Job status
/api/health                    # Health check
```

**Route Groups** (App Router):
- `(auth)/` - Protected routes requiring authentication
- `(public)/` - Public-facing pages (landing, documentation)
- `api/` - API endpoints for data operations

## Component Architecture

### Server Components

**When to Use**:
- Initial data fetching from databases
- SEO-important content
- Static or slowly-changing content
- Direct database queries

**Example** (Neo4j data fetching):
```typescript
// app/documents/page.tsx (Server Component)
import { neo4jClient } from '@/lib/neo4j';

export default async function DocumentsPage() {
  // Fetch documents from Neo4j on the server
  const documents = await neo4jClient.executeQuery(`
    MATCH (m:Metadata)-[:METADATA_FOR]->(d:Document)
    RETURN m, d
    ORDER BY m.processed_at DESC
    LIMIT 50
  `);

  return (
    <div>
      <h1>Documents</h1>
      <DocumentList documents={documents} />
    </div>
  );
}
```

### Client Components

**When to Use**:
- Interactive components (buttons, forms, modals)
- Browser APIs (window, localStorage)
- Event handlers (onClick, onChange)
- React hooks (useState, useEffect)
- Animation and transitions

**Example** (File upload component):
```typescript
'use client';

import { useState } from 'react';
import { Upload, File, X } from 'lucide-react';

export function FileUpload({ onFilesSelected }: { onFilesSelected: (files: File[]) => void }) {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    setSelectedFiles(files);
    onFilesSelected(files);
  };

  return (
    <div className="border-2 border-dashed rounded-lg p-8">
      <input
        type="file"
        multiple
        onChange={handleFileChange}
        className="hidden"
        id="file-upload"
      />
      <label htmlFor="file-upload" className="cursor-pointer">
        <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
        <p className="text-center">Click to upload files</p>
      </label>

      {selectedFiles.length > 0 && (
        <div className="mt-4">
          {selectedFiles.map((file, idx) => (
            <div key={idx} className="flex items-center gap-2">
              <File className="w-4 h-4" />
              <span>{file.name}</span>
              <span className="text-sm text-gray-500">({(file.size / 1024).toFixed(2)} KB)</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

### Shared Components

**UI Component Library** (`components/ui/`):
- `Button.tsx` - Reusable button component
- `Card.tsx` - Card container
- `Input.tsx` - Form input
- `Select.tsx` - Dropdown select
- `Modal.tsx` - Modal dialog
- `Badge.tsx` - Status badges
- `ProgressBar.tsx` - Progress indicators
- `Spinner.tsx` - Loading spinner

**Tremor Components** (Data Visualization):
- `<Card>` - Data cards
- `<BarChart>` - Bar charts
- `<DonutChart>` - Donut charts
- `<AreaChart>` - Area charts
- `<Badge>` - Status badges
- `<Metric>` - Key metrics display

## Five-Step User Pipeline UI

### Step 1: Document Upload (`UploadWizard.tsx`)

**Component**: `components/upload/FileUpload.tsx`

**Features**:
- Drag-and-drop file upload
- Multiple file selection
- File type validation (PDF, DOCX, TXT, MD)
- File size validation (max 100MB per file)
- Preview selected files
- Remove files from selection

**Implementation**:
```typescript
interface FileUploadProps {
  onFilesSelected: (files: File[]) => void;
  maxFileSize?: number;
  acceptedFileTypes?: string[];
}

export function FileUpload({
  onFilesSelected,
  maxFileSize = 100 * 1024 * 1024, // 100MB
  acceptedFileTypes = ['.pdf', '.docx', '.txt', '.md']
}: FileUploadProps) {
  // Drag-and-drop handling
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    validateAndAddFiles(files);
  };

  // File validation
  const validateAndAddFiles = (files: File[]) => {
    const validFiles = files.filter(file => {
      if (file.size > maxFileSize) {
        alert(`File ${file.name} exceeds maximum size of 100MB`);
        return false;
      }
      return true;
    });
    onFilesSelected(validFiles);
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      className="border-2 border-dashed rounded-lg p-8"
    >
      {/* Upload UI */}
    </div>
  );
}
```

### Step 2: Entity Configuration (`EntityConfigStep.tsx`)

**Component**: `components/upload/EntityConfigStep.tsx`

**Features**:
- Select entity types to extract (18 total)
- Industrial entities: VENDOR, PROTOCOL, STANDARD, COMPONENT, MEASUREMENT, ORGANIZATION, SAFETY_CLASS, SYSTEM_LAYER
- Cybersecurity entities: CVE, CWE, CAPEC, THREAT_ACTOR, CAMPAIGN, ATTACK_TECHNIQUE, MALWARE, IOC, APT_GROUP
- Select all/deselect all
- Entity type descriptions

**Implementation**:
```typescript
const ENTITY_TYPES = [
  { id: 'VENDOR', category: 'Industrial', description: 'Equipment/software vendors' },
  { id: 'PROTOCOL', category: 'Industrial', description: 'Communication protocols' },
  { id: 'CVE', category: 'Cybersecurity', description: 'Common Vulnerabilities and Exposures' },
  { id: 'MALWARE', category: 'Cybersecurity', description: 'Malware families' },
  // ... 18 total
];

export function EntityConfigStep({ onEntityTypesSelected }: { onEntityTypesSelected: (types: string[]) => void }) {
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);

  const toggleEntityType = (typeId: string) => {
    setSelectedTypes(prev =>
      prev.includes(typeId) ? prev.filter(t => t !== typeId) : [...prev, typeId]
    );
  };

  useEffect(() => {
    onEntityTypesSelected(selectedTypes);
  }, [selectedTypes]);

  return (
    <div className="grid grid-cols-2 gap-4">
      {ENTITY_TYPES.map(type => (
        <div
          key={type.id}
          className={`p-4 border rounded cursor-pointer ${
            selectedTypes.includes(type.id) ? 'bg-blue-50 border-blue-500' : ''
          }`}
          onClick={() => toggleEntityType(type.id)}
        >
          <h3 className="font-semibold">{type.id}</h3>
          <p className="text-sm text-gray-600">{type.description}</p>
          <span className="text-xs text-gray-500">{type.category}</span>
        </div>
      ))}
    </div>
  );
}
```

### Step 3: Relationship Configuration (`RelationshipConfigStep.tsx`)

**Component**: `components/upload/RelationshipConfigStep.tsx`

**Features**:
- Select relationship types to extract
- Predefined relationship types (WORKS_FOR, LOCATED_IN, USES, etc.)
- Custom relationship type input
- Relationship directionality

**Implementation**:
```typescript
const RELATIONSHIP_TYPES = [
  'WORKS_FOR', 'LOCATED_IN', 'USES', 'MANAGES', 'CONTAINS', 'DEPENDS_ON',
  'COMMUNICATES_WITH', 'EXPLOITS', 'MITIGATES'
];

export function RelationshipConfigStep({ onRelationshipsSelected }: { onRelationshipsSelected: (types: string[]) => void }) {
  const [selectedRelationships, setSelectedRelationships] = useState<string[]>([]);

  return (
    <div>
      <h2>Select Relationship Types</h2>
      <div className="grid grid-cols-3 gap-2">
        {RELATIONSHIP_TYPES.map(type => (
          <button
            key={type}
            onClick={() => toggleRelationship(type)}
            className={`p-2 border rounded ${selectedRelationships.includes(type) ? 'bg-blue-500 text-white' : ''}`}
          >
            {type}
          </button>
        ))}
      </div>
    </div>
  );
}
```

### Step 4: Processing Status (`ProcessingStep.tsx`)

**Component**: `components/upload/ProcessingStep.tsx`

**Features**:
- Real-time job progress tracking
- Three-stage progress display (Classification, NER, Ingestion)
- Progress bars for each stage
- Status messages
- Error handling
- Cancel job option

**Implementation**:
```typescript
'use client';

import { useEffect, useState } from 'react';
import { ProgressBar } from '@/components/ui/ProgressBar';

interface JobStatus {
  jobId: string;
  status: 'queued' | 'classifying' | 'extracting' | 'ingesting' | 'complete' | 'failed';
  progress: number;
  message: string;
  steps: {
    classification: { status: string; progress: number };
    ner: { status: string; progress: number };
    ingestion: { status: string; progress: number };
  };
}

export function ProcessingStep({ jobId }: { jobId: string }) {
  const [jobStatus, setJobStatus] = useState<JobStatus | null>(null);

  useEffect(() => {
    // Poll job status every 2 seconds
    const interval = setInterval(async () => {
      const response = await fetch(`/api/pipeline/status/${jobId}`);
      const data = await response.json();
      setJobStatus(data);

      // Stop polling when complete or failed
      if (data.status === 'complete' || data.status === 'failed') {
        clearInterval(interval);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId]);

  if (!jobStatus) return <div>Loading...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Processing Document</h2>
        <p className="text-gray-600">{jobStatus.message}</p>
      </div>

      <div className="space-y-4">
        {/* Classification Step */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="font-medium">Classification</span>
            <span className="text-sm text-gray-500">{jobStatus.steps.classification.status}</span>
          </div>
          <ProgressBar progress={jobStatus.steps.classification.progress} />
        </div>

        {/* NER Step */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="font-medium">Entity Extraction</span>
            <span className="text-sm text-gray-500">{jobStatus.steps.ner.status}</span>
          </div>
          <ProgressBar progress={jobStatus.steps.ner.progress} />
        </div>

        {/* Ingestion Step */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="font-medium">Graph Ingestion</span>
            <span className="text-sm text-gray-500">{jobStatus.steps.ingestion.status}</span>
          </div>
          <ProgressBar progress={jobStatus.steps.ingestion.progress} />
        </div>
      </div>

      {/* Overall Progress */}
      <div>
        <div className="flex justify-between items-center mb-2">
          <span className="font-semibold">Overall Progress</span>
          <span className="font-semibold">{jobStatus.progress}%</span>
        </div>
        <ProgressBar progress={jobStatus.progress} size="lg" />
      </div>

      {/* Status Badge */}
      {jobStatus.status === 'complete' && (
        <div className="bg-green-50 border border-green-500 rounded p-4">
          <p className="text-green-700 font-semibold">✓ Processing Complete!</p>
        </div>
      )}

      {jobStatus.status === 'failed' && (
        <div className="bg-red-50 border border-red-500 rounded p-4">
          <p className="text-red-700 font-semibold">✗ Processing Failed</p>
          <p className="text-sm text-red-600">{jobStatus.message}</p>
        </div>
      )}
    </div>
  );
}
```

### Step 5: Results Visualization

**Component**: `components/upload/ResultsStep.tsx` (redirects to graph view)

**Features**:
- Summary of extracted entities
- Entity counts by type
- Graph visualization preview
- Navigation to full graph view
- Export options (JSON, CSV)

## API Integration

### REST Endpoints

**File Upload** (`/api/upload`):
```typescript
// app/api/upload/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { minioClient } from '@/lib/minio';
import { auth } from '@clerk/nextjs';

export async function POST(req: NextRequest) {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const formData = await req.formData();
  const files = formData.getAll('files') as File[];

  const uploadedFiles = await Promise.all(
    files.map(async (file) => {
      const buffer = Buffer.from(await file.arrayBuffer());
      const filename = `uploads/${new Date().toISOString()}_${file.name}`;

      await minioClient.putObject('aeon-documents', filename, buffer, buffer.length, {
        'Content-Type': file.type
      });

      return {
        originalName: file.name,
        path: filename,
        size: file.size,
        type: file.type
      };
    })
  );

  return NextResponse.json({ success: true, files: uploadedFiles });
}
```

**Pipeline Processing** (`/api/pipeline/process`):
```typescript
// app/api/pipeline/process/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { addJob } from '@/lib/queue/documentQueue';

export async function POST(req: NextRequest) {
  const body = await req.json();
  const { files, customer, tags, classification } = body;

  // Validation
  if (!files || files.length === 0) {
    return NextResponse.json({ error: 'No files provided' }, { status: 400 });
  }

  // Submit jobs
  const jobs = await Promise.all(
    files.map(async (file: any) => {
      const jobId = await addJob({
        fileName: file.name,
        filePath: file.path,
        customer,
        tags,
        classification,
        fileSize: file.size,
        fileType: file.type
      });

      return {
        jobId,
        status: 'queued',
        progress: 0,
        message: `Queued: ${file.name}`,
        fileName: file.name
      };
    })
  );

  return NextResponse.json({ success: true, jobs, message: `Started processing ${files.length} file(s)` });
}
```

**Job Status** (`/api/pipeline/status/[jobId]`):
```typescript
// app/api/pipeline/status/[jobId]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { getJobStatus } from '@/lib/queue/documentQueue';

export async function GET(
  req: NextRequest,
  { params }: { params: { jobId: string } }
) {
  const jobStatus = getJobStatus(params.jobId);

  if (!jobStatus) {
    return NextResponse.json({ error: 'Job not found' }, { status: 404 });
  }

  return NextResponse.json({ success: true, ...jobStatus });
}
```

### Error Handling

**Global Error Boundary**:
```typescript
// app/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
        <p className="text-gray-600 mb-4">{error.message}</p>
        <button
          onClick={reset}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Try again
        </button>
      </div>
    </div>
  );
}
```

**API Error Handling**:
```typescript
// lib/utils/apiClient.ts
export async function apiRequest<T>(url: string, options?: RequestInit): Promise<T> {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers
      }
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'API request failed');
    }

    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}
```

## Authentication & Authorization

### Clerk Integration

**Setup** (`app/layout.tsx`):
```typescript
import { ClerkProvider } from '@clerk/nextjs';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

**Protected Routes** (`middleware.ts`):
```typescript
import { authMiddleware } from '@clerk/nextjs';

export default authMiddleware({
  publicRoutes: ['/', '/api/health'],
  ignoredRoutes: ['/api/webhook']
});

export const config = {
  matcher: ['/((?!.+\\.[\\w]+$|_next).*)', '/', '/(api|trpc)(.*)'],
};
```

**User Authentication Check**:
```typescript
import { auth, currentUser } from '@clerk/nextjs';

export default async function ProtectedPage() {
  const { userId } = await auth();
  const user = await currentUser();

  if (!userId) {
    redirect('/sign-in');
  }

  return <div>Welcome {user?.firstName}!</div>;
}
```

## Performance Optimization

### Code Splitting

**Dynamic Imports**:
```typescript
import dynamic from 'next/dynamic';

// Lazy load heavy components
const GraphVisualization = dynamic(() => import('@/components/graph/GraphVisualization'), {
  loading: () => <Spinner />,
  ssr: false
});
```

**Route-based Splitting**: Next.js 15 automatically splits code by route

### Image Optimization

**Next.js Image Component**:
```typescript
import Image from 'next/image';

<Image
  src="/logo.png"
  alt="AEON DT Logo"
  width={200}
  height={50}
  priority
/>
```

### Caching Strategy

**Server Component Caching** (default in Next.js 15):
```typescript
// Revalidate every hour
export const revalidate = 3600;

export default async function DocumentsPage() {
  const documents = await fetchDocuments();
  return <DocumentList documents={documents} />;
}
```

**Client-side Caching** (SWR pattern):
```typescript
import useSWR from 'swr';

function useJobStatus(jobId: string) {
  const { data, error } = useSWR(
    `/api/pipeline/status/${jobId}`,
    fetcher,
    { refreshInterval: 2000 }
  );

  return {
    jobStatus: data,
    isLoading: !error && !data,
    isError: error
  };
}
```

## Accessibility

**WCAG Compliance Features**:
- Semantic HTML
- ARIA labels and roles
- Keyboard navigation
- Focus management
- Color contrast (AA standard)
- Screen reader support

**Example** (Accessible form):
```typescript
<label htmlFor="file-upload" className="block text-sm font-medium">
  Upload Document
</label>
<input
  id="file-upload"
  type="file"
  aria-describedby="file-upload-description"
  className="..."
/>
<p id="file-upload-description" className="text-sm text-gray-500">
  Accepted formats: PDF, DOCX, TXT, MD (max 100MB)
</p>
```

## Testing Strategy

### Unit Tests (Vitest)

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { FileUpload } from '@/components/upload/FileUpload';

describe('FileUpload', () => {
  it('should call onFilesSelected when files are selected', () => {
    const mockOnFilesSelected = vi.fn();
    render(<FileUpload onFilesSelected={mockOnFilesSelected} />);

    const input = screen.getByLabelText('Upload files');
    const file = new File(['test'], 'test.pdf', { type: 'application/pdf' });

    fireEvent.change(input, { target: { files: [file] } });

    expect(mockOnFilesSelected).toHaveBeenCalledWith([file]);
  });
});
```

### Integration Tests (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('complete upload workflow', async ({ page }) => {
  await page.goto('/upload');

  // Step 1: Upload file
  await page.setInputFiles('input[type="file"]', 'test.pdf');
  await page.click('button:has-text("Next")');

  // Step 2: Classification
  await page.selectOption('[name="sector"]', 'Infrastructure');
  await page.click('button:has-text("Next")');

  // Step 3: Entity configuration
  await page.click('text=VENDOR');
  await page.click('text=PROTOCOL');
  await page.click('button:has-text("Next")');

  // Step 4: Submit
  await page.click('button:has-text("Process Document")');

  // Step 5: Wait for completion
  await expect(page.locator('text=Processing Complete')).toBeVisible({ timeout: 60000 });
});
```

### E2E Tests

```typescript
test('end-to-end document processing', async ({ page }) => {
  // Login
  await page.goto('/sign-in');
  await page.fill('[name="identifier"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button:has-text("Sign in")');

  // Upload document
  await page.goto('/upload');
  await page.setInputFiles('input[type="file"]', 'technical_spec.pdf');
  // ... complete wizard steps ...

  // Verify in Neo4j
  const jobId = await page.locator('[data-testid="job-id"]').textContent();

  // Wait for processing
  await page.waitForSelector('text=Processing Complete');

  // Navigate to graph view
  await page.goto('/graph');
  await expect(page.locator('text=Siemens')).toBeVisible();
});
```

---

## Component Dependencies

**Key Package Versions** (from package.json):
```json
{
  "dependencies": {
    "next": "15.0.3",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@clerk/nextjs": "^6.7.3",
    "@tremor/react": "^3.18.5",
    "framer-motion": "^11.18.0",
    "lucide-react": "^0.468.0",
    "minio": "^8.0.2",
    "neo4j-driver": "^5.27.0",
    "tailwindcss": "^3.4.1",
    "typescript": "^5"
  },
  "devDependencies": {
    "@types/react": "^19",
    "@playwright/test": "^1.40.0",
    "vitest": "^1.0.0"
  }
}
```

## Environment Configuration

**Required Environment Variables** (`.env.local`):
```bash
# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard

# MinIO Configuration
MINIO_ENDPOINT=openspg-minio
MINIO_PORT=9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio@openspg
MINIO_BUCKET=aeon-documents

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:3000/api
```

---

*Next.js 15 Frontend Documentation | AEON DT v1.0.0 | 2025-11-11*
*Framework: App Router | React 19 | TypeScript 5*
