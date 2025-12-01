# Original Data Ingestion Pipeline UI Requirements

**Document**: Data Ingestion Pipeline Web Interface Specification
**Date Created**: 2025-11-03 (Reconstructed from previous discussions)
**Status**: FAILED WITH STREAMLIT, READY FOR NEXT.JS IMPLEMENTATION
**Purpose**: Web interface for managing Neo4j data ingestion pipeline

---

## Executive Summary

This document captures the original requirements for the Data Ingestion Pipeline UI that was attempted with Streamlit and failed. The requirements are now being preserved for re-implementation using the successful Next.js + Tremor React stack.

**What Happened**:
- Original attempt: Streamlit-based web interface
- Result: Complete failure due to import conflicts, heavy ML dependencies, poor architecture
- Current status: Next.js infrastructure deployed successfully
- Next step: Implement these features in Next.js

---

## Original Requirements Overview

### Core Purpose
Build a web-based UI for managing the complete data ingestion pipeline from source documents into Neo4j knowledge graph, with real-time monitoring, visualization, and control capabilities.

### Target Users
- Data engineers managing document ingestion
- Analysts monitoring knowledge graph population
- Administrators overseeing pipeline health
- Researchers querying ingested data

---

## Functional Requirements

### 1. Document Upload & Management

#### File Upload Interface
**Purpose**: Upload documents for processing into Neo4j knowledge graph

**Features Required**:
- [ ] Drag-and-drop file upload area
- [ ] Multi-file upload support (batch processing)
- [ ] Supported formats: PDF, TXT, MD, DOCX, JSON, CSV
- [ ] File size validation (max 50MB per file)
- [ ] Upload progress tracking with percentage
- [ ] File preview before processing
- [ ] Metadata tagging (source, category, date, author)
- [ ] Duplicate file detection

**UI Components**:
```typescript
// Upload component structure
<FileUploadZone>
  <DragDropArea />
  <FileList>
    <FileItem status="pending|processing|completed|failed" />
  </FileList>
  <ProgressBar />
  <MetadataForm />
</FileUploadZone>
```

#### Document Queue Management
**Purpose**: Manage pending documents awaiting processing

**Features Required**:
- [ ] View all queued documents
- [ ] Prioritize documents (high/medium/low priority)
- [ ] Pause/resume document processing
- [ ] Cancel pending documents
- [ ] Retry failed documents
- [ ] Batch operations (delete, prioritize, retry)
- [ ] Filter by status (pending, processing, completed, failed)
- [ ] Sort by date, priority, size, type

**Data Model**:
```typescript
interface Document {
  id: string;
  filename: string;
  fileType: string;
  size: number;
  uploadDate: Date;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  priority: 'low' | 'medium' | 'high';
  metadata: {
    source?: string;
    category?: string;
    author?: string;
    tags?: string[];
  };
  processedEntities?: number;
  processedRelationships?: number;
  errorMessage?: string;
}
```

---

### 2. Processing Pipeline Dashboard

#### Real-Time Processing Monitor
**Purpose**: Monitor document processing in real-time

**Features Required**:
- [ ] Live processing status dashboard
- [ ] Current document being processed
- [ ] Processing stage indicator (extraction → analysis → graph creation)
- [ ] Processing speed metrics (docs/hour, entities/second)
- [ ] Resource usage (CPU, memory, Neo4j connections)
- [ ] Active worker threads status
- [ ] Queue depth visualization
- [ ] Estimated time remaining for queue

**Visualization Components**:
```typescript
<ProcessingDashboard>
  <CurrentProcessing document={current} stage="extraction" />
  <MetricsPanel>
    <Metric name="Processing Speed" value="120 entities/sec" />
    <Metric name="Queue Depth" value="47 documents" />
    <Metric name="ETA" value="2h 15m" />
  </MetricsPanel>
  <ResourceGauges>
    <Gauge name="CPU" value={75} max={100} />
    <Gauge name="Memory" value={12} max={16} unit="GB" />
    <Gauge name="Neo4j Connections" value={15} max={50} />
  </ResourceGauges>
  <ProcessingStages>
    <Stage name="NLP Extraction" status="active" />
    <Stage name="Entity Resolution" status="pending" />
    <Stage name="Graph Writing" status="pending" />
  </ProcessingStages>
</ProcessingDashboard>
```

#### Processing History & Logs
**Purpose**: Review past processing operations

**Features Required**:
- [ ] Complete processing history
- [ ] Filterable logs (by date, status, document type)
- [ ] Detailed processing logs for each document
- [ ] Error logs with stack traces
- [ ] Processing time analytics
- [ ] Success/failure rate charts
- [ ] Export logs to CSV/JSON

---

### 3. Neo4j Integration Dashboard

#### Knowledge Graph Statistics
**Purpose**: Display current state of Neo4j knowledge graph

**Features Required**:
- [ ] Total entities count by type
- [ ] Total relationships count by type
- [ ] Graph growth charts (entities over time, relationships over time)
- [ ] Recent entities added (live feed)
- [ ] Schema overview (node labels, relationship types)
- [ ] Property statistics
- [ ] Index health status
- [ ] Constraint violations

**Statistics Display**:
```typescript
<KnowledgeGraphStats>
  <StatCards>
    <Card title="Total Entities" value="12,256" trend="+450" />
    <Card title="Total Relationships" value="14,645" trend="+523" />
    <Card title="Documents Processed" value="115" trend="+5" />
  </StatCards>

  <EntityBreakdown>
    <BarChart data={entityTypes} />
    {/* Person: 3,245, Organization: 1,890, Concept: 7,121 */}
  </EntityBreakdown>

  <RelationshipBreakdown>
    <PieChart data={relationshipTypes} />
    {/* RELATED_TO: 8,234, MEMBER_OF: 2,145, HAS_TRAIT: 4,266 */}
  </RelationshipBreakdown>

  <GrowthTimeline>
    <AreaChart data={growthOverTime} />
  </GrowthTimeline>
</KnowledgeGraphStats>
```

#### Live Graph Visualization
**Purpose**: Interactive visualization of knowledge graph

**Features Required**:
- [ ] Interactive network graph (using Neovis.js or similar)
- [ ] Node filtering by type
- [ ] Relationship filtering by type
- [ ] Search nodes by name/property
- [ ] Expand/collapse nodes
- [ ] Zoom and pan controls
- [ ] Node clustering
- [ ] Shortest path visualization
- [ ] Community detection visualization

**Implementation**:
```typescript
<GraphVisualization>
  <ControlPanel>
    <NodeTypeFilter types={['Person', 'Organization', 'Concept']} />
    <RelationshipFilter types={['RELATED_TO', 'MEMBER_OF']} />
    <SearchBar placeholder="Search nodes..." />
    <LayoutSelector options={['force', 'hierarchical', 'circular']} />
  </ControlPanel>

  <NeovisCanvas
    config={{
      serverUrl: "bolt://openspg-neo4j:7687",
      serverUser: "neo4j",
      serverPassword: "neo4j@openspg",
      initialCypher: "MATCH (n) RETURN n LIMIT 100"
    }}
  />
</GraphVisualization>
```

---

### 4. Data Quality & Validation

#### Quality Metrics Dashboard
**Purpose**: Monitor data quality during ingestion

**Features Required**:
- [ ] Entity extraction accuracy metrics
- [ ] Relationship confidence scores
- [ ] Duplicate detection alerts
- [ ] Missing data warnings
- [ ] Schema validation errors
- [ ] Data consistency checks
- [ ] Quality score trending

**Metrics Display**:
```typescript
<QualityDashboard>
  <QualityScore overall={87} />

  <MetricsGrid>
    <Metric
      name="Entity Extraction Accuracy"
      value={92}
      threshold={90}
      status="good"
    />
    <Metric
      name="Relationship Confidence"
      value={85}
      threshold={80}
      status="good"
    />
    <Metric
      name="Duplicate Entities Detected"
      value={23}
      threshold={50}
      status="warning"
    />
    <Metric
      name="Schema Violations"
      value={2}
      threshold={0}
      status="error"
    />
  </MetricsGrid>

  <ValidationResults>
    <IssueList>
      <Issue
        type="warning"
        message="23 potential duplicate entities detected"
        action="Review duplicates"
      />
      <Issue
        type="error"
        message="2 entities missing required properties"
        action="Fix schema violations"
      />
    </IssueList>
  </ValidationResults>
</QualityDashboard>
```

#### Data Validation Rules
**Purpose**: Configure and manage validation rules

**Features Required**:
- [ ] Create custom validation rules
- [ ] Enable/disable validation rules
- [ ] Validation rule testing
- [ ] Validation rule priorities
- [ ] Automatic data cleaning rules
- [ ] Manual review queue for flagged data

---

### 5. Configuration & Settings

#### Pipeline Configuration
**Purpose**: Configure data ingestion pipeline parameters

**Features Required**:
- [ ] NLP model selection (spaCy model, embeddings model)
- [ ] Entity extraction thresholds
- [ ] Relationship extraction confidence levels
- [ ] Batch size configuration
- [ ] Parallel processing workers
- [ ] Retry policies
- [ ] Error handling strategies

**Configuration UI**:
```typescript
<PipelineConfig>
  <Section title="NLP Configuration">
    <Select
      label="spaCy Model"
      options={['en_core_web_sm', 'en_core_web_lg']}
      default="en_core_web_lg"
    />
    <Select
      label="Embeddings Model"
      options={['all-MiniLM-L6-v2', 'all-mpnet-base-v2']}
      default="all-MiniLM-L6-v2"
    />
  </Section>

  <Section title="Extraction Thresholds">
    <Slider
      label="Entity Confidence Threshold"
      min={0}
      max={1}
      step={0.05}
      default={0.7}
    />
    <Slider
      label="Relationship Confidence Threshold"
      min={0}
      max={1}
      step={0.05}
      default={0.6}
    />
  </Section>

  <Section title="Performance">
    <NumberInput
      label="Batch Size"
      min={1}
      max={100}
      default={10}
    />
    <NumberInput
      label="Worker Threads"
      min={1}
      max={16}
      default={4}
    />
  </Section>
</PipelineConfig>
```

#### Neo4j Connection Settings
**Purpose**: Manage Neo4j database connections

**Features Required**:
- [ ] Connection string configuration
- [ ] Credentials management (encrypted)
- [ ] Connection testing
- [ ] Connection pooling settings
- [ ] Transaction batch size
- [ ] Timeout configurations

---

### 6. Search & Query Interface

#### Cypher Query Builder
**Purpose**: Build and execute Cypher queries visually

**Features Required**:
- [ ] Visual query builder (drag-and-drop)
- [ ] Cypher syntax editor with autocomplete
- [ ] Query templates (common patterns)
- [ ] Query history
- [ ] Save favorite queries
- [ ] Export results to CSV/JSON
- [ ] Query performance profiling

**Query Builder UI**:
```typescript
<QueryBuilder>
  <QueryComposer>
    <VisualBuilder>
      <NodeSelector />
      <RelationshipSelector />
      <PropertyFilter />
      <ReturnSelector />
    </VisualBuilder>

    <CypherEditor
      value={cypherQuery}
      autocomplete={true}
      syntax="cypher"
    />
  </QueryComposer>

  <ResultsPanel>
    <ResultsTable data={queryResults} />
    <ResultsVisualization type="graph|table|json" />
    <ExportButton formats={['csv', 'json', 'cypher']} />
  </ResultsPanel>

  <QueryHistory>
    <HistoryItem query="MATCH (p:Person) RETURN p LIMIT 10" />
  </QueryHistory>
</QueryBuilder>
```

#### Full-Text Search
**Purpose**: Search across all ingested documents

**Features Required**:
- [ ] Full-text search across all entities
- [ ] Filter by entity type
- [ ] Filter by source document
- [ ] Filter by date range
- [ ] Fuzzy matching
- [ ] Boolean operators (AND, OR, NOT)
- [ ] Search result highlighting
- [ ] Related entities suggestions

---

### 7. Reporting & Analytics

#### Ingestion Reports
**Purpose**: Generate reports on data ingestion activities

**Features Required**:
- [ ] Daily/weekly/monthly ingestion summaries
- [ ] Processing performance reports
- [ ] Error analysis reports
- [ ] Data quality trend reports
- [ ] Custom report builder
- [ ] Scheduled report generation
- [ ] Email report delivery
- [ ] Export reports to PDF

#### Analytics Dashboard
**Purpose**: Visualize trends and insights

**Features Required**:
- [ ] Entity growth trends
- [ ] Relationship growth trends
- [ ] Processing throughput charts
- [ ] Error rate trending
- [ ] Peak processing times
- [ ] Resource utilization heatmaps
- [ ] Comparative analytics (week-over-week, month-over-month)

---

## Non-Functional Requirements

### Performance Requirements
- [ ] **Page Load Time**: < 2 seconds for initial load
- [ ] **Real-Time Updates**: Update dashboard metrics every 5 seconds
- [ ] **Large File Upload**: Support files up to 50MB
- [ ] **Concurrent Users**: Support 20+ simultaneous users
- [ ] **Graph Visualization**: Render graphs with 1000+ nodes smoothly

### Security Requirements
- [ ] **Authentication**: NextAuth.js with multiple providers
- [ ] **Authorization**: Role-based access control (Admin, Editor, Viewer)
- [ ] **Data Encryption**: HTTPS/TLS for all communications
- [ ] **Credential Storage**: Encrypted storage for Neo4j credentials
- [ ] **Session Management**: Secure session handling with timeout
- [ ] **Audit Logging**: Log all data modifications

### Reliability Requirements
- [ ] **Uptime**: 99.5% availability target
- [ ] **Error Recovery**: Graceful handling of Neo4j disconnections
- [ ] **Data Integrity**: Transactional processing with rollback capability
- [ ] **Backup**: Automatic state preservation

### Usability Requirements
- [ ] **Responsive Design**: Work on desktop, tablet, mobile
- [ ] **Accessibility**: WCAG 2.1 Level AA compliance
- [ ] **Browser Support**: Chrome, Firefox, Safari, Edge (latest 2 versions)
- [ ] **Loading States**: Clear feedback during async operations
- [ ] **Error Messages**: User-friendly error messages with resolution steps

---

## Technical Architecture

### Technology Stack (Current - Next.js Implementation)
```yaml
frontend:
  framework: Next.js 15.5.6
  ui_library: Tremor React 3.18.7
  styling: Tailwind CSS 3.4.14
  language: TypeScript 5.6.3

backend:
  runtime: Node.js 20
  api: Next.js API Routes

databases:
  neo4j:
    driver: neo4j-driver 5.25.0
    uri: bolt://openspg-neo4j:7687
  qdrant:
    client: @qdrant/js-client-rest 1.12.0
    uri: http://openspg-qdrant:6333
  mysql:
    client: mysql2 3.11.3
    uri: openspg-mysql:3306
  minio:
    client: minio 8.0.1
    uri: http://openspg-minio:9000

visualization:
  graphs: Neovis.js or vis.js
  charts: Tremor (Recharts)
  tables: Tremor DataTable

deployment:
  container: Docker
  network: openspg-network
  port: 3000
```

### Data Flow Architecture
```
User Upload → File Validation → Queue Management →
  ↓
Processing Pipeline:
  1. NLP Extraction (spaCy, Transformers)
  2. Entity Resolution
  3. Relationship Extraction
  4. Neo4j Write
  ↓
Knowledge Graph Update → Dashboard Update → User Notification
```

---

## Implementation Phases

### Phase 1: Core Infrastructure (COMPLETED ✅)
- [x] Next.js application setup
- [x] Docker containerization
- [x] Database connectivity (Neo4j, Qdrant, MySQL, MinIO)
- [x] Health check API
- [x] Basic homepage with metrics

### Phase 2: Document Upload & Queue (NEXT)
- [ ] File upload component with drag-and-drop
- [ ] Document queue management interface
- [ ] Processing status tracking
- [ ] File metadata management
- [ ] Basic processing pipeline integration

### Phase 3: Processing Dashboard
- [ ] Real-time processing monitor
- [ ] Processing metrics dashboard
- [ ] Resource usage gauges
- [ ] Processing logs viewer
- [ ] Error handling UI

### Phase 4: Neo4j Integration
- [ ] Knowledge graph statistics
- [ ] Entity/relationship breakdown charts
- [ ] Live graph visualization with Neovis.js
- [ ] Schema overview display
- [ ] Graph growth trending

### Phase 5: Data Quality & Validation
- [ ] Quality metrics dashboard
- [ ] Validation rule configuration
- [ ] Duplicate detection interface
- [ ] Data review queue
- [ ] Manual correction tools

### Phase 6: Search & Query
- [ ] Visual Cypher query builder
- [ ] Cypher editor with autocomplete
- [ ] Full-text search interface
- [ ] Query history management
- [ ] Result export functionality

### Phase 7: Reporting & Analytics
- [ ] Report builder interface
- [ ] Analytics visualizations
- [ ] Scheduled reports
- [ ] Custom dashboard builder

---

## Why Streamlit Failed

### Technical Failures
1. **Import Conflicts**: Two `utils` packages caused Python import hell
2. **Heavy Dependencies**: Loading 10GB+ ML models (spaCy) for UI layer
3. **Architecture Coupling**: UI layer importing entire agent ecosystem
4. **Production Readiness**: Streamlit not designed for production deployment
5. **Docker Issues**: Complex dependency tree prevented containerization
6. **Performance**: Slow rendering, heavy resource usage
7. **Limited Customization**: Difficult to achieve desired UX

### Why Next.js Will Succeed
1. **Clean Separation**: UI layer only imports database clients
2. **Focused Dependencies**: 198 production packages, all necessary
3. **Production-Ready**: Docker, standalone mode, optimized builds
4. **Modern Stack**: TypeScript, Tailwind, React 18, Tremor
5. **Excellent Ecosystem**: Rich component libraries, visualization tools
6. **Performance**: SSR, optimized routing, fast builds
7. **Flexibility**: Full control over UI/UX

---

## Success Criteria

### Functional Success
- [ ] Upload and process 100+ documents successfully
- [ ] Real-time dashboard updates within 5 seconds
- [ ] Graph visualization renders 1000+ nodes
- [ ] Cypher queries execute in < 2 seconds
- [ ] Zero data loss during processing
- [ ] 95%+ entity extraction accuracy

### User Experience Success
- [ ] Intuitive UI requiring no training
- [ ] Mobile-responsive on all devices
- [ ] Accessible to users with disabilities
- [ ] Clear error messages and recovery paths
- [ ] Fast page loads (< 2 seconds)

### Technical Success
- [ ] 99.5% uptime
- [ ] Handles 20+ concurrent users
- [ ] Processes 1000+ documents/day
- [ ] Zero security vulnerabilities
- [ ] Complete audit trail
- [ ] Automated backups

---

## Appendices

### Appendix A: Data Models

#### Document Processing Status
```typescript
interface ProcessingStatus {
  documentId: string;
  stage: 'queued' | 'extracting' | 'resolving' | 'writing' | 'complete' | 'failed';
  progress: number; // 0-100
  startTime: Date;
  endTime?: Date;
  extractedEntities: number;
  extractedRelationships: number;
  errors: ProcessingError[];
}
```

#### Entity Extraction Result
```typescript
interface ExtractedEntity {
  id: string;
  text: string;
  type: 'Person' | 'Organization' | 'Concept' | 'Location' | 'Event';
  confidence: number;
  properties: Record<string, any>;
  source: {
    documentId: string;
    startOffset: number;
    endOffset: number;
  };
}
```

#### Relationship Extraction Result
```typescript
interface ExtractedRelationship {
  id: string;
  sourceEntityId: string;
  targetEntityId: string;
  type: string;
  confidence: number;
  properties: Record<string, any>;
  source: {
    documentId: string;
    context: string;
  };
}
```

### Appendix B: API Endpoints

```typescript
// Document Management
POST   /api/documents/upload        // Upload new documents
GET    /api/documents/queue         // Get processing queue
POST   /api/documents/{id}/priority // Update document priority
DELETE /api/documents/{id}          // Remove document from queue

// Processing
GET    /api/processing/status       // Get current processing status
POST   /api/processing/start        // Start processing
POST   /api/processing/pause        // Pause processing
POST   /api/processing/cancel/{id}  // Cancel specific document

// Neo4j Statistics
GET    /api/neo4j/stats             // Get graph statistics
GET    /api/neo4j/entities          // List entities with pagination
GET    /api/neo4j/relationships     // List relationships
POST   /api/neo4j/query             // Execute Cypher query

// Quality & Validation
GET    /api/quality/metrics         // Get quality metrics
GET    /api/quality/issues          // Get validation issues
POST   /api/quality/rules           // Create validation rule

// Reports
POST   /api/reports/generate        // Generate custom report
GET    /api/reports/history         // Get report history
```

---

**Document Status**: READY FOR IMPLEMENTATION
**Next Action**: Begin Phase 2 - Document Upload & Queue Interface
**Target Start Date**: 2025-11-04
**Estimated Completion**: 4-6 weeks for full implementation
