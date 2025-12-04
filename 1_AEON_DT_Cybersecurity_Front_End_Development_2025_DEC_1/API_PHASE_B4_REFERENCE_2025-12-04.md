# Phase B4 Frontend API Reference Documentation

**Document ID**: API_PHASE_B4_REFERENCE
**Date**: 2025-12-04
**Status**: PRODUCTION READY
**Phase**: B4 - Compliance & Automation
**Version**: 1.0.0

---

## Overview

Phase B4 introduces comprehensive compliance mapping, automated scanning, and advanced alert management capabilities to the AEON Cybersecurity Platform.

### API Summary

| Enhancement | Base Path | Endpoints | Status | Description |
|------------|-----------|-----------|--------|-------------|
| E07 Compliance Mapping | `/api/v2/compliance` | 28 | LIVE | Framework mapping, control tracking, evidence management |
| E08 Automated Scanning | `/api/v2/scanning` | 30 | LIVE | Vulnerability scanning, schedule management, findings analysis |
| E09 Alert Management | `/api/v2/alerts` | 32 | LIVE | Alert rules, notifications, escalation policies, correlation |
| **Total** | - | **90** | **LIVE** | Complete compliance and automation suite |

---

## Table of Contents

1. [E07 Compliance Mapping API](#e07-compliance-mapping-api)
2. [E08 Automated Scanning API](#e08-automated-scanning-api)
3. [E09 Alert Management API](#e09-alert-management-api)
4. [React Hooks](#react-hooks)
5. [API Client Examples](#api-client-examples)
6. [Integration Patterns](#integration-patterns)
7. [Qdrant Collections](#qdrant-collections)

---

## E07 Compliance Mapping API

### Base Path
```
/api/v2/compliance
```

### TypeScript Interfaces

#### Enums

```typescript
export enum ComplianceFramework {
  NERC_CIP = 'NERC_CIP',
  NIST_CSF = 'NIST_CSF',
  ISO_27001 = 'ISO_27001',
  SOC2 = 'SOC2',
  PCI_DSS = 'PCI_DSS',
  HIPAA = 'HIPAA',
  GDPR = 'GDPR',
  CIS_CONTROLS = 'CIS_CONTROLS'
}

export enum ComplianceStatus {
  COMPLIANT = 'compliant',
  PARTIAL = 'partial',
  NON_COMPLIANT = 'non_compliant',
  NOT_APPLICABLE = 'not_applicable',
  IN_PROGRESS = 'in_progress',
  PENDING_REVIEW = 'pending_review'
}

export enum ControlCategory {
  ACCESS_CONTROL = 'access_control',
  ASSET_MANAGEMENT = 'asset_management',
  CRYPTOGRAPHY = 'cryptography',
  PHYSICAL_SECURITY = 'physical_security',
  OPERATIONS = 'operations',
  COMMUNICATIONS = 'communications',
  ACQUISITION = 'acquisition',
  INCIDENT_RESPONSE = 'incident_response',
  BUSINESS_CONTINUITY = 'business_continuity',
  COMPLIANCE = 'compliance'
}

export enum EvidenceType {
  DOCUMENT = 'document',
  SCREENSHOT = 'screenshot',
  LOG_FILE = 'log_file',
  CONFIGURATION = 'configuration',
  SCAN_RESULT = 'scan_result',
  POLICY = 'policy',
  PROCEDURE = 'procedure',
  ATTESTATION = 'attestation'
}

export enum AssessmentStatus {
  SCHEDULED = 'scheduled',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}
```

#### Core Interfaces

```typescript
export interface ComplianceControl {
  id: string;
  framework: ComplianceFramework;
  controlId: string;
  title: string;
  description: string;
  category: ControlCategory;
  requirements: string[];
  implementationGuidance: string;
  testingProcedures: string[];
  references: string[];
  relatedControls: string[];
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface ComplianceMapping {
  id: string;
  controlId: string;
  assetId: string;
  assetType: 'device' | 'network' | 'application' | 'data';
  status: ComplianceStatus;
  implementationDetails: string;
  responsibleParty: string;
  reviewDate: string;
  nextReviewDate: string;
  evidenceIds: string[];
  gaps: ComplianceGap[];
  remediationPlan?: string;
  notes: string;
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface ComplianceAssessment {
  id: string;
  framework: ComplianceFramework;
  name: string;
  description: string;
  startDate: string;
  endDate: string;
  status: AssessmentStatus;
  scope: {
    frameworks: ComplianceFramework[];
    assetIds: string[];
    controlIds: string[];
  };
  assessor: string;
  findings: AssessmentFinding[];
  overallScore: number;
  reportUrl?: string;
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface AssessmentFinding {
  controlId: string;
  status: ComplianceStatus;
  evidence: string[];
  gaps: string[];
  recommendations: string[];
  severity: 'critical' | 'high' | 'medium' | 'low';
  remediationEffort: 'low' | 'medium' | 'high';
}

export interface ComplianceEvidence {
  id: string;
  controlId: string;
  type: EvidenceType;
  title: string;
  description: string;
  fileUrl: string;
  uploadedBy: string;
  uploadDate: string;
  expirationDate?: string;
  tags: string[];
  metadata: Record<string, any>;
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface ComplianceGap {
  id: string;
  controlId: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  impact: string;
  recommendedActions: string[];
  estimatedEffort: string;
  targetDate?: string;
  assignedTo?: string;
  status: 'open' | 'in_progress' | 'resolved' | 'accepted';
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface ComplianceReport {
  id: string;
  framework: ComplianceFramework;
  reportType: 'summary' | 'detailed' | 'executive' | 'audit';
  generatedDate: string;
  reportingPeriod: {
    startDate: string;
    endDate: string;
  };
  overallCompliance: number;
  controlsSummary: {
    total: number;
    compliant: number;
    partial: number;
    nonCompliant: number;
    notApplicable: number;
  };
  criticalGaps: ComplianceGap[];
  recommendations: string[];
  reportUrl: string;
  customerId: string;
}
```

#### Request/Response Types

```typescript
// Controls
export interface CreateControlRequest {
  framework: ComplianceFramework;
  controlId: string;
  title: string;
  description: string;
  category: ControlCategory;
  requirements: string[];
  implementationGuidance: string;
  testingProcedures?: string[];
  references?: string[];
}

export interface UpdateControlRequest {
  title?: string;
  description?: string;
  requirements?: string[];
  implementationGuidance?: string;
  testingProcedures?: string[];
  references?: string[];
}

export interface ListControlsRequest {
  framework?: ComplianceFramework;
  category?: ControlCategory;
  search?: string;
  page?: number;
  limit?: number;
}

export interface ListControlsResponse {
  controls: ComplianceControl[];
  total: number;
  page: number;
  limit: number;
}

// Mappings
export interface CreateMappingRequest {
  controlId: string;
  assetId: string;
  assetType: 'device' | 'network' | 'application' | 'data';
  status: ComplianceStatus;
  implementationDetails: string;
  responsibleParty: string;
  reviewDate: string;
}

export interface UpdateMappingRequest {
  status?: ComplianceStatus;
  implementationDetails?: string;
  responsibleParty?: string;
  reviewDate?: string;
  evidenceIds?: string[];
  notes?: string;
}

export interface ListMappingsRequest {
  controlId?: string;
  assetId?: string;
  status?: ComplianceStatus;
  framework?: ComplianceFramework;
  page?: number;
  limit?: number;
}

export interface ListMappingsResponse {
  mappings: ComplianceMapping[];
  total: number;
  page: number;
  limit: number;
}

// Assessments
export interface CreateAssessmentRequest {
  framework: ComplianceFramework;
  name: string;
  description: string;
  startDate: string;
  endDate: string;
  scope: {
    frameworks: ComplianceFramework[];
    assetIds?: string[];
    controlIds?: string[];
  };
  assessor: string;
}

export interface UpdateAssessmentRequest {
  name?: string;
  description?: string;
  startDate?: string;
  endDate?: string;
  status?: AssessmentStatus;
  findings?: AssessmentFinding[];
}

export interface ListAssessmentsRequest {
  framework?: ComplianceFramework;
  status?: AssessmentStatus;
  startDate?: string;
  endDate?: string;
  page?: number;
  limit?: number;
}

export interface ListAssessmentsResponse {
  assessments: ComplianceAssessment[];
  total: number;
  page: number;
  limit: number;
}

// Evidence
export interface CreateEvidenceRequest {
  controlId: string;
  type: EvidenceType;
  title: string;
  description: string;
  fileUrl: string;
  expirationDate?: string;
  tags?: string[];
  metadata?: Record<string, any>;
}

export interface UpdateEvidenceRequest {
  title?: string;
  description?: string;
  expirationDate?: string;
  tags?: string[];
  metadata?: Record<string, any>;
}

export interface ListEvidenceRequest {
  controlId?: string;
  type?: EvidenceType;
  tags?: string[];
  expiringWithinDays?: number;
  page?: number;
  limit?: number;
}

export interface ListEvidenceResponse {
  evidence: ComplianceEvidence[];
  total: number;
  page: number;
  limit: number;
}

// Gaps
export interface CreateGapRequest {
  controlId: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  impact: string;
  recommendedActions: string[];
  estimatedEffort: string;
  targetDate?: string;
  assignedTo?: string;
}

export interface UpdateGapRequest {
  description?: string;
  severity?: 'critical' | 'high' | 'medium' | 'low';
  impact?: string;
  recommendedActions?: string[];
  estimatedEffort?: string;
  targetDate?: string;
  assignedTo?: string;
  status?: 'open' | 'in_progress' | 'resolved' | 'accepted';
}

export interface ListGapsRequest {
  controlId?: string;
  severity?: 'critical' | 'high' | 'medium' | 'low';
  status?: 'open' | 'in_progress' | 'resolved' | 'accepted';
  assignedTo?: string;
  page?: number;
  limit?: number;
}

export interface ListGapsResponse {
  gaps: ComplianceGap[];
  total: number;
  page: number;
  limit: number;
}

// Reports
export interface GenerateReportRequest {
  framework: ComplianceFramework;
  reportType: 'summary' | 'detailed' | 'executive' | 'audit';
  reportingPeriod: {
    startDate: string;
    endDate: string;
  };
  includeEvidence?: boolean;
  includeGaps?: boolean;
  includeRecommendations?: boolean;
}

export interface GenerateReportResponse {
  report: ComplianceReport;
}

export interface ListReportsRequest {
  framework?: ComplianceFramework;
  reportType?: 'summary' | 'detailed' | 'executive' | 'audit';
  startDate?: string;
  endDate?: string;
  page?: number;
  limit?: number;
}

export interface ListReportsResponse {
  reports: ComplianceReport[];
  total: number;
  page: number;
  limit: number;
}
```

### API Endpoints

```typescript
// Controls
GET    /api/v2/compliance/controls              // List controls
POST   /api/v2/compliance/controls              // Create control
GET    /api/v2/compliance/controls/:id          // Get control
PUT    /api/v2/compliance/controls/:id          // Update control
DELETE /api/v2/compliance/controls/:id          // Delete control

// Mappings
GET    /api/v2/compliance/mappings              // List mappings
POST   /api/v2/compliance/mappings              // Create mapping
GET    /api/v2/compliance/mappings/:id          // Get mapping
PUT    /api/v2/compliance/mappings/:id          // Update mapping
DELETE /api/v2/compliance/mappings/:id          // Delete mapping
GET    /api/v2/compliance/mappings/asset/:assetId  // Get asset mappings

// Assessments
GET    /api/v2/compliance/assessments           // List assessments
POST   /api/v2/compliance/assessments           // Create assessment
GET    /api/v2/compliance/assessments/:id       // Get assessment
PUT    /api/v2/compliance/assessments/:id       // Update assessment
DELETE /api/v2/compliance/assessments/:id       // Delete assessment
POST   /api/v2/compliance/assessments/:id/start // Start assessment
POST   /api/v2/compliance/assessments/:id/complete  // Complete assessment

// Evidence
GET    /api/v2/compliance/evidence              // List evidence
POST   /api/v2/compliance/evidence              // Create evidence
GET    /api/v2/compliance/evidence/:id          // Get evidence
PUT    /api/v2/compliance/evidence/:id          // Update evidence
DELETE /api/v2/compliance/evidence/:id          // Delete evidence
GET    /api/v2/compliance/evidence/expiring     // Get expiring evidence

// Gaps
GET    /api/v2/compliance/gaps                  // List gaps
POST   /api/v2/compliance/gaps                  // Create gap
GET    /api/v2/compliance/gaps/:id              // Get gap
PUT    /api/v2/compliance/gaps/:id              // Update gap
DELETE /api/v2/compliance/gaps/:id              // Delete gap

// Reports
GET    /api/v2/compliance/reports               // List reports
POST   /api/v2/compliance/reports               // Generate report
GET    /api/v2/compliance/reports/:id           // Get report
DELETE /api/v2/compliance/reports/:id           // Delete report

// Dashboard
GET    /api/v2/compliance/dashboard             // Get compliance dashboard
GET    /api/v2/compliance/dashboard/framework/:framework  // Framework-specific dashboard
```

---

## E08 Automated Scanning API

### Base Path
```
/api/v2/scanning
```

### TypeScript Interfaces

#### Enums

```typescript
export enum ScanType {
  VULNERABILITY = 'vulnerability',
  COMPLIANCE = 'compliance',
  CONFIGURATION = 'configuration',
  NETWORK = 'network',
  APPLICATION = 'application',
  DATABASE = 'database',
  CLOUD = 'cloud',
  CONTAINER = 'container'
}

export enum ScanStatus {
  SCHEDULED = 'scheduled',
  QUEUED = 'queued',
  RUNNING = 'running',
  PAUSED = 'paused',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

export enum ScannerType {
  NMAP = 'nmap',
  NESSUS = 'nessus',
  OPENVAS = 'openvas',
  QUALYS = 'qualys',
  BURP = 'burp',
  OWASP_ZAP = 'owasp_zap',
  TRIVY = 'trivy',
  CLAIR = 'clair',
  CUSTOM = 'custom'
}

export enum ScanFrequency {
  ONCE = 'once',
  HOURLY = 'hourly',
  DAILY = 'daily',
  WEEKLY = 'weekly',
  MONTHLY = 'monthly',
  QUARTERLY = 'quarterly'
}

export enum FindingSeverity {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
  INFO = 'info'
}

export enum FindingStatus {
  NEW = 'new',
  CONFIRMED = 'confirmed',
  FALSE_POSITIVE = 'false_positive',
  IN_REMEDIATION = 'in_remediation',
  REMEDIATED = 'remediated',
  ACCEPTED = 'accepted',
  REOPEN = 'reopen'
}
```

#### Core Interfaces

```typescript
export interface ScanProfile {
  id: string;
  name: string;
  description: string;
  type: ScanType;
  scanner: ScannerType;
  configuration: {
    scanSettings: Record<string, any>;
    plugins?: string[];
    policies?: string[];
    exclusions?: string[];
    customOptions?: Record<string, any>;
  };
  targetCriteria: {
    assetTags?: string[];
    assetTypes?: string[];
    networkRanges?: string[];
    specificAssets?: string[];
  };
  notificationSettings: {
    onStart?: boolean;
    onComplete?: boolean;
    onError?: boolean;
    onFindings?: boolean;
    recipients?: string[];
  };
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface ScanSchedule {
  id: string;
  profileId: string;
  name: string;
  description: string;
  frequency: ScanFrequency;
  schedule: {
    cronExpression?: string;
    dayOfWeek?: number[];
    dayOfMonth?: number[];
    hour?: number;
    minute?: number;
    timezone?: string;
  };
  enabled: boolean;
  startDate: string;
  endDate?: string;
  lastRunDate?: string;
  nextRunDate?: string;
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface ScanJob {
  id: string;
  profileId: string;
  scheduleId?: string;
  name: string;
  type: ScanType;
  status: ScanStatus;
  startTime: string;
  endTime?: string;
  duration?: number;
  progress: number;
  targets: ScanTarget[];
  findings: {
    total: number;
    critical: number;
    high: number;
    medium: number;
    low: number;
    info: number;
  };
  errors: string[];
  metadata: Record<string, any>;
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface ScanTarget {
  id: string;
  assetId: string;
  assetName: string;
  assetType: string;
  ipAddress?: string;
  hostname?: string;
  status: 'pending' | 'scanning' | 'completed' | 'failed';
  progress: number;
  findings: number;
  startTime?: string;
  endTime?: string;
}

export interface ScanFinding {
  id: string;
  jobId: string;
  targetId: string;
  type: ScanType;
  title: string;
  description: string;
  severity: FindingSeverity;
  status: FindingStatus;
  cvssScore?: number;
  cvssVector?: string;
  cveId?: string;
  cweId?: string;
  affectedComponent: string;
  vulnerability: {
    name: string;
    description: string;
    solution?: string;
    references?: string[];
    exploitAvailable?: boolean;
    patchAvailable?: boolean;
  };
  evidence: {
    type: string;
    data: string;
    location: string;
  }[];
  remediation: {
    recommendation: string;
    effort: 'low' | 'medium' | 'high';
    priority: number;
    steps?: string[];
  };
  assignedTo?: string;
  dueDate?: string;
  notes: string;
  customerId: string;
  firstDetected: string;
  lastDetected: string;
  createdAt: string;
  updatedAt: string;
}

export interface ScanReport {
  id: string;
  jobId: string;
  reportType: 'executive' | 'technical' | 'compliance' | 'detailed';
  format: 'pdf' | 'html' | 'json' | 'csv';
  generatedDate: string;
  summary: {
    totalTargets: number;
    totalFindings: number;
    criticalFindings: number;
    highFindings: number;
    mediumFindings: number;
    lowFindings: number;
    infoFindings: number;
    remediatedFindings: number;
  };
  topVulnerabilities: ScanFinding[];
  complianceStatus?: Record<string, any>;
  reportUrl: string;
  customerId: string;
}
```

#### Request/Response Types

```typescript
// Profiles
export interface CreateProfileRequest {
  name: string;
  description: string;
  type: ScanType;
  scanner: ScannerType;
  configuration: {
    scanSettings: Record<string, any>;
    plugins?: string[];
    policies?: string[];
    exclusions?: string[];
  };
  targetCriteria: {
    assetTags?: string[];
    assetTypes?: string[];
    networkRanges?: string[];
    specificAssets?: string[];
  };
  notificationSettings?: {
    onStart?: boolean;
    onComplete?: boolean;
    onError?: boolean;
    recipients?: string[];
  };
}

export interface UpdateProfileRequest {
  name?: string;
  description?: string;
  configuration?: Partial<ScanProfile['configuration']>;
  targetCriteria?: Partial<ScanProfile['targetCriteria']>;
  notificationSettings?: Partial<ScanProfile['notificationSettings']>;
}

export interface ListProfilesRequest {
  type?: ScanType;
  scanner?: ScannerType;
  search?: string;
  page?: number;
  limit?: number;
}

export interface ListProfilesResponse {
  profiles: ScanProfile[];
  total: number;
  page: number;
  limit: number;
}

// Schedules
export interface CreateScheduleRequest {
  profileId: string;
  name: string;
  description: string;
  frequency: ScanFrequency;
  schedule: {
    cronExpression?: string;
    dayOfWeek?: number[];
    dayOfMonth?: number[];
    hour?: number;
    minute?: number;
    timezone?: string;
  };
  enabled?: boolean;
  startDate: string;
  endDate?: string;
}

export interface UpdateScheduleRequest {
  name?: string;
  description?: string;
  frequency?: ScanFrequency;
  schedule?: Partial<ScanSchedule['schedule']>;
  enabled?: boolean;
  startDate?: string;
  endDate?: string;
}

export interface ListSchedulesRequest {
  profileId?: string;
  frequency?: ScanFrequency;
  enabled?: boolean;
  page?: number;
  limit?: number;
}

export interface ListSchedulesResponse {
  schedules: ScanSchedule[];
  total: number;
  page: number;
  limit: number;
}

// Jobs
export interface CreateJobRequest {
  profileId: string;
  name: string;
  scheduleId?: string;
  startImmediately?: boolean;
  targets?: {
    assetIds?: string[];
    networkRanges?: string[];
  };
}

export interface UpdateJobRequest {
  status?: ScanStatus;
  metadata?: Record<string, any>;
}

export interface ListJobsRequest {
  profileId?: string;
  scheduleId?: string;
  type?: ScanType;
  status?: ScanStatus;
  startDate?: string;
  endDate?: string;
  page?: number;
  limit?: number;
}

export interface ListJobsResponse {
  jobs: ScanJob[];
  total: number;
  page: number;
  limit: number;
}

// Findings
export interface CreateFindingRequest {
  jobId: string;
  targetId: string;
  type: ScanType;
  title: string;
  description: string;
  severity: FindingSeverity;
  cvssScore?: number;
  cveId?: string;
  affectedComponent: string;
  vulnerability: {
    name: string;
    description: string;
    solution?: string;
    references?: string[];
  };
  evidence: {
    type: string;
    data: string;
    location: string;
  }[];
}

export interface UpdateFindingRequest {
  status?: FindingStatus;
  severity?: FindingSeverity;
  assignedTo?: string;
  dueDate?: string;
  notes?: string;
}

export interface ListFindingsRequest {
  jobId?: string;
  type?: ScanType;
  severity?: FindingSeverity;
  status?: FindingStatus;
  assignedTo?: string;
  cveId?: string;
  page?: number;
  limit?: number;
}

export interface ListFindingsResponse {
  findings: ScanFinding[];
  total: number;
  page: number;
  limit: number;
}

// Reports
export interface GenerateScanReportRequest {
  jobId: string;
  reportType: 'executive' | 'technical' | 'compliance' | 'detailed';
  format: 'pdf' | 'html' | 'json' | 'csv';
  includeEvidence?: boolean;
  includeRemediation?: boolean;
}

export interface GenerateScanReportResponse {
  report: ScanReport;
}

export interface ListScanReportsRequest {
  jobId?: string;
  reportType?: 'executive' | 'technical' | 'compliance' | 'detailed';
  startDate?: string;
  endDate?: string;
  page?: number;
  limit?: number;
}

export interface ListScanReportsResponse {
  reports: ScanReport[];
  total: number;
  page: number;
  limit: number;
}
```

### API Endpoints

```typescript
// Profiles
GET    /api/v2/scanning/profiles                // List profiles
POST   /api/v2/scanning/profiles                // Create profile
GET    /api/v2/scanning/profiles/:id            // Get profile
PUT    /api/v2/scanning/profiles/:id            // Update profile
DELETE /api/v2/scanning/profiles/:id            // Delete profile
POST   /api/v2/scanning/profiles/:id/validate   // Validate profile

// Schedules
GET    /api/v2/scanning/schedules               // List schedules
POST   /api/v2/scanning/schedules               // Create schedule
GET    /api/v2/scanning/schedules/:id           // Get schedule
PUT    /api/v2/scanning/schedules/:id           // Update schedule
DELETE /api/v2/scanning/schedules/:id           // Delete schedule
POST   /api/v2/scanning/schedules/:id/enable    // Enable schedule
POST   /api/v2/scanning/schedules/:id/disable   // Disable schedule

// Jobs
GET    /api/v2/scanning/jobs                    // List jobs
POST   /api/v2/scanning/jobs                    // Create job
GET    /api/v2/scanning/jobs/:id                // Get job
PUT    /api/v2/scanning/jobs/:id                // Update job
DELETE /api/v2/scanning/jobs/:id                // Delete job
POST   /api/v2/scanning/jobs/:id/start          // Start job
POST   /api/v2/scanning/jobs/:id/pause          // Pause job
POST   /api/v2/scanning/jobs/:id/resume         // Resume job
POST   /api/v2/scanning/jobs/:id/cancel         // Cancel job
GET    /api/v2/scanning/jobs/:id/progress       // Get job progress

// Findings
GET    /api/v2/scanning/findings                // List findings
POST   /api/v2/scanning/findings                // Create finding
GET    /api/v2/scanning/findings/:id            // Get finding
PUT    /api/v2/scanning/findings/:id            // Update finding
DELETE /api/v2/scanning/findings/:id            // Delete finding
POST   /api/v2/scanning/findings/:id/remediate  // Mark remediated
POST   /api/v2/scanning/findings/:id/accept     // Accept risk
GET    /api/v2/scanning/findings/trending       // Get trending findings

// Reports
GET    /api/v2/scanning/reports                 // List reports
POST   /api/v2/scanning/reports                 // Generate report
GET    /api/v2/scanning/reports/:id             // Get report
DELETE /api/v2/scanning/reports/:id             // Delete report

// Dashboard
GET    /api/v2/scanning/dashboard               // Get scanning dashboard
GET    /api/v2/scanning/dashboard/metrics       // Get scan metrics
```

---

## E09 Alert Management API

### Base Path
```
/api/v2/alerts
```

### TypeScript Interfaces

#### Enums

```typescript
export enum AlertSeverity {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
  INFO = 'info'
}

export enum AlertStatus {
  NEW = 'new',
  ACKNOWLEDGED = 'acknowledged',
  INVESTIGATING = 'investigating',
  RESOLVED = 'resolved',
  CLOSED = 'closed',
  SUPPRESSED = 'suppressed'
}

export enum AlertCategory {
  SECURITY = 'security',
  PERFORMANCE = 'performance',
  AVAILABILITY = 'availability',
  COMPLIANCE = 'compliance',
  CONFIGURATION = 'configuration',
  CAPACITY = 'capacity',
  ANOMALY = 'anomaly',
  SYSTEM = 'system'
}

export enum NotificationChannel {
  EMAIL = 'email',
  SMS = 'sms',
  SLACK = 'slack',
  TEAMS = 'teams',
  PAGERDUTY = 'pagerduty',
  WEBHOOK = 'webhook',
  MOBILE_PUSH = 'mobile_push'
}

export enum RuleOperator {
  EQUALS = 'equals',
  NOT_EQUALS = 'not_equals',
  GREATER_THAN = 'greater_than',
  LESS_THAN = 'less_than',
  CONTAINS = 'contains',
  NOT_CONTAINS = 'not_contains',
  REGEX = 'regex',
  IN = 'in',
  NOT_IN = 'not_in'
}

export enum AggregationMethod {
  COUNT = 'count',
  SUM = 'sum',
  AVERAGE = 'average',
  MIN = 'min',
  MAX = 'max',
  DISTINCT = 'distinct'
}
```

#### Core Interfaces

```typescript
export interface Alert {
  id: string;
  ruleId: string;
  ruleName: string;
  title: string;
  description: string;
  severity: AlertSeverity;
  category: AlertCategory;
  status: AlertStatus;
  source: {
    type: 'device' | 'network' | 'application' | 'scan' | 'system';
    id: string;
    name: string;
    metadata: Record<string, any>;
  };
  context: {
    metric?: string;
    value?: any;
    threshold?: any;
    additionalData?: Record<string, any>;
  };
  triggeredAt: string;
  acknowledgedAt?: string;
  acknowledgedBy?: string;
  resolvedAt?: string;
  resolvedBy?: string;
  closedAt?: string;
  closedBy?: string;
  assignedTo?: string;
  escalationLevel: number;
  correlationId?: string;
  relatedAlerts: string[];
  notifications: AlertNotification[];
  timeline: AlertTimelineEvent[];
  tags: string[];
  notes: string;
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface AlertNotification {
  id: string;
  channel: NotificationChannel;
  recipient: string;
  sentAt: string;
  status: 'pending' | 'sent' | 'failed' | 'delivered';
  errorMessage?: string;
}

export interface AlertTimelineEvent {
  timestamp: string;
  action: string;
  user?: string;
  details: string;
}

export interface AlertRule {
  id: string;
  name: string;
  description: string;
  category: AlertCategory;
  severity: AlertSeverity;
  enabled: boolean;
  conditions: RuleCondition[];
  conditionLogic: 'AND' | 'OR';
  aggregation?: {
    method: AggregationMethod;
    timeWindow: number;
    threshold: number;
  };
  filters: {
    assetTags?: string[];
    assetTypes?: string[];
    timeRange?: {
      start: string;
      end: string;
    };
  };
  actions: RuleAction[];
  cooldownPeriod?: number;
  maxAlertsPerDay?: number;
  suppressionRules?: SuppressionRule[];
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface RuleCondition {
  field: string;
  operator: RuleOperator;
  value: any;
  valueType: 'string' | 'number' | 'boolean' | 'array';
}

export interface RuleAction {
  type: 'notify' | 'execute' | 'update' | 'escalate';
  config: Record<string, any>;
}

export interface SuppressionRule {
  id: string;
  reason: string;
  conditions: RuleCondition[];
  startTime?: string;
  endTime?: string;
}

export interface NotificationRule {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  triggers: {
    alertSeverity?: AlertSeverity[];
    alertCategory?: AlertCategory[];
    alertStatus?: AlertStatus[];
    ruleIds?: string[];
  };
  channels: NotificationChannelConfig[];
  schedule?: {
    enabled: boolean;
    timeZone: string;
    businessHours?: {
      days: number[];
      startHour: number;
      endHour: number;
    };
    excludedDates?: string[];
  };
  recipients: NotificationRecipient[];
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface NotificationChannelConfig {
  channel: NotificationChannel;
  enabled: boolean;
  config: Record<string, any>;
  retryPolicy?: {
    maxRetries: number;
    retryDelay: number;
  };
}

export interface NotificationRecipient {
  id: string;
  name: string;
  type: 'user' | 'group' | 'role';
  channels: {
    email?: string;
    sms?: string;
    slack?: string;
    teams?: string;
  };
}

export interface EscalationPolicy {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  triggers: {
    noAcknowledgment: number;
    noResolution: number;
    severityIncrease?: boolean;
  };
  levels: EscalationLevel[];
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface EscalationLevel {
  level: number;
  delayMinutes: number;
  recipients: string[];
  channels: NotificationChannel[];
  requireAcknowledgment: boolean;
}

export interface AlertCorrelation {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  correlationKey: string;
  timeWindow: number;
  minAlertCount: number;
  patterns: CorrelationPattern[];
  actions: RuleAction[];
  customerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface CorrelationPattern {
  id: string;
  type: 'sequence' | 'concurrent' | 'threshold' | 'anomaly';
  conditions: RuleCondition[];
  weight: number;
}

export interface AlertStatistics {
  totalAlerts: number;
  alertsBySeverity: Record<AlertSeverity, number>;
  alertsByCategory: Record<AlertCategory, number>;
  alertsByStatus: Record<AlertStatus, number>;
  meanTimeToAcknowledge: number;
  meanTimeToResolve: number;
  topAlertRules: Array<{
    ruleId: string;
    ruleName: string;
    count: number;
  }>;
  topAlertSources: Array<{
    sourceId: string;
    sourceName: string;
    count: number;
  }>;
  trendData: Array<{
    date: string;
    count: number;
    severity: AlertSeverity;
  }>;
}
```

#### Request/Response Types

```typescript
// Alerts
export interface CreateAlertRequest {
  ruleId: string;
  title: string;
  description: string;
  severity: AlertSeverity;
  category: AlertCategory;
  source: {
    type: 'device' | 'network' | 'application' | 'scan' | 'system';
    id: string;
    name: string;
    metadata?: Record<string, any>;
  };
  context?: {
    metric?: string;
    value?: any;
    threshold?: any;
    additionalData?: Record<string, any>;
  };
  tags?: string[];
}

export interface UpdateAlertRequest {
  status?: AlertStatus;
  severity?: AlertSeverity;
  assignedTo?: string;
  notes?: string;
  tags?: string[];
}

export interface AcknowledgeAlertRequest {
  acknowledgedBy: string;
  notes?: string;
}

export interface ResolveAlertRequest {
  resolvedBy: string;
  resolution: string;
  rootCause?: string;
  preventiveMeasures?: string;
}

export interface ListAlertsRequest {
  severity?: AlertSeverity;
  category?: AlertCategory;
  status?: AlertStatus;
  ruleId?: string;
  sourceId?: string;
  assignedTo?: string;
  startDate?: string;
  endDate?: string;
  search?: string;
  page?: number;
  limit?: number;
}

export interface ListAlertsResponse {
  alerts: Alert[];
  total: number;
  page: number;
  limit: number;
}

// Alert Rules
export interface CreateAlertRuleRequest {
  name: string;
  description: string;
  category: AlertCategory;
  severity: AlertSeverity;
  enabled?: boolean;
  conditions: RuleCondition[];
  conditionLogic: 'AND' | 'OR';
  aggregation?: {
    method: AggregationMethod;
    timeWindow: number;
    threshold: number;
  };
  filters?: {
    assetTags?: string[];
    assetTypes?: string[];
  };
  actions: RuleAction[];
  cooldownPeriod?: number;
  maxAlertsPerDay?: number;
}

export interface UpdateAlertRuleRequest {
  name?: string;
  description?: string;
  severity?: AlertSeverity;
  enabled?: boolean;
  conditions?: RuleCondition[];
  conditionLogic?: 'AND' | 'OR';
  aggregation?: Partial<AlertRule['aggregation']>;
  filters?: Partial<AlertRule['filters']>;
  actions?: RuleAction[];
  cooldownPeriod?: number;
  maxAlertsPerDay?: number;
}

export interface ListAlertRulesRequest {
  category?: AlertCategory;
  severity?: AlertSeverity;
  enabled?: boolean;
  search?: string;
  page?: number;
  limit?: number;
}

export interface ListAlertRulesResponse {
  rules: AlertRule[];
  total: number;
  page: number;
  limit: number;
}

// Notification Rules
export interface CreateNotificationRuleRequest {
  name: string;
  description: string;
  enabled?: boolean;
  triggers: {
    alertSeverity?: AlertSeverity[];
    alertCategory?: AlertCategory[];
    alertStatus?: AlertStatus[];
    ruleIds?: string[];
  };
  channels: NotificationChannelConfig[];
  schedule?: {
    enabled: boolean;
    timeZone: string;
    businessHours?: {
      days: number[];
      startHour: number;
      endHour: number;
    };
  };
  recipients: NotificationRecipient[];
}

export interface UpdateNotificationRuleRequest {
  name?: string;
  description?: string;
  enabled?: boolean;
  triggers?: Partial<NotificationRule['triggers']>;
  channels?: NotificationChannelConfig[];
  schedule?: Partial<NotificationRule['schedule']>;
  recipients?: NotificationRecipient[];
}

export interface ListNotificationRulesRequest {
  enabled?: boolean;
  channel?: NotificationChannel;
  page?: number;
  limit?: number;
}

export interface ListNotificationRulesResponse {
  rules: NotificationRule[];
  total: number;
  page: number;
  limit: number;
}

// Escalation Policies
export interface CreateEscalationPolicyRequest {
  name: string;
  description: string;
  enabled?: boolean;
  triggers: {
    noAcknowledgment: number;
    noResolution: number;
    severityIncrease?: boolean;
  };
  levels: EscalationLevel[];
}

export interface UpdateEscalationPolicyRequest {
  name?: string;
  description?: string;
  enabled?: boolean;
  triggers?: Partial<EscalationPolicy['triggers']>;
  levels?: EscalationLevel[];
}

export interface ListEscalationPoliciesRequest {
  enabled?: boolean;
  page?: number;
  limit?: number;
}

export interface ListEscalationPoliciesResponse {
  policies: EscalationPolicy[];
  total: number;
  page: number;
  limit: number;
}

// Correlation
export interface CreateCorrelationRequest {
  name: string;
  description: string;
  enabled?: boolean;
  correlationKey: string;
  timeWindow: number;
  minAlertCount: number;
  patterns: CorrelationPattern[];
  actions: RuleAction[];
}

export interface UpdateCorrelationRequest {
  name?: string;
  description?: string;
  enabled?: boolean;
  correlationKey?: string;
  timeWindow?: number;
  minAlertCount?: number;
  patterns?: CorrelationPattern[];
  actions?: RuleAction[];
}

export interface ListCorrelationsRequest {
  enabled?: boolean;
  page?: number;
  limit?: number;
}

export interface ListCorrelationsResponse {
  correlations: AlertCorrelation[];
  total: number;
  page: number;
  limit: number;
}

// Statistics
export interface GetStatisticsRequest {
  startDate: string;
  endDate: string;
  severity?: AlertSeverity;
  category?: AlertCategory;
  groupBy?: 'day' | 'week' | 'month';
}

export interface GetStatisticsResponse {
  statistics: AlertStatistics;
}
```

### API Endpoints

```typescript
// Alerts
GET    /api/v2/alerts                           // List alerts
POST   /api/v2/alerts                           // Create alert
GET    /api/v2/alerts/:id                       // Get alert
PUT    /api/v2/alerts/:id                       // Update alert
DELETE /api/v2/alerts/:id                       // Delete alert
POST   /api/v2/alerts/:id/acknowledge           // Acknowledge alert
POST   /api/v2/alerts/:id/resolve               // Resolve alert
POST   /api/v2/alerts/:id/close                 // Close alert
POST   /api/v2/alerts/:id/escalate              // Escalate alert
POST   /api/v2/alerts/:id/suppress              // Suppress alert
POST   /api/v2/alerts/bulk/acknowledge          // Bulk acknowledge
POST   /api/v2/alerts/bulk/resolve              // Bulk resolve

// Alert Rules
GET    /api/v2/alerts/rules                     // List rules
POST   /api/v2/alerts/rules                     // Create rule
GET    /api/v2/alerts/rules/:id                 // Get rule
PUT    /api/v2/alerts/rules/:id                 // Update rule
DELETE /api/v2/alerts/rules/:id                 // Delete rule
POST   /api/v2/alerts/rules/:id/enable          // Enable rule
POST   /api/v2/alerts/rules/:id/disable         // Disable rule
POST   /api/v2/alerts/rules/:id/test            // Test rule

// Notification Rules
GET    /api/v2/alerts/notifications             // List notification rules
POST   /api/v2/alerts/notifications             // Create notification rule
GET    /api/v2/alerts/notifications/:id         // Get notification rule
PUT    /api/v2/alerts/notifications/:id         // Update notification rule
DELETE /api/v2/alerts/notifications/:id         // Delete notification rule
POST   /api/v2/alerts/notifications/:id/test    // Test notification

// Escalation Policies
GET    /api/v2/alerts/escalations               // List escalation policies
POST   /api/v2/alerts/escalations               // Create escalation policy
GET    /api/v2/alerts/escalations/:id           // Get escalation policy
PUT    /api/v2/alerts/escalations/:id           // Update escalation policy
DELETE /api/v2/alerts/escalations/:id           // Delete escalation policy

// Correlation
GET    /api/v2/alerts/correlations              // List correlations
POST   /api/v2/alerts/correlations              // Create correlation
GET    /api/v2/alerts/correlations/:id          // Get correlation
PUT    /api/v2/alerts/correlations/:id          // Update correlation
DELETE /api/v2/alerts/correlations/:id          // Delete correlation
GET    /api/v2/alerts/correlations/:id/matches  // Get correlated alerts

// Statistics
GET    /api/v2/alerts/statistics                // Get alert statistics
GET    /api/v2/alerts/statistics/trending       // Get trending alerts
GET    /api/v2/alerts/statistics/mttr           // Get MTTR metrics
GET    /api/v2/alerts/statistics/mtta           // Get MTTA metrics
```

---

## React Hooks

### E07 Compliance Hooks

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ComplianceControl,
  ComplianceMapping,
  ComplianceAssessment,
  ComplianceEvidence,
  ComplianceGap,
  ComplianceFramework,
  CreateControlRequest,
  CreateMappingRequest,
  CreateAssessmentRequest,
} from './types';

// Controls
export function useComplianceControls(params?: ListControlsRequest) {
  return useQuery({
    queryKey: ['compliance', 'controls', params],
    queryFn: () => apiClient.compliance.listControls(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useComplianceControl(id: string) {
  return useQuery({
    queryKey: ['compliance', 'controls', id],
    queryFn: () => apiClient.compliance.getControl(id),
    enabled: !!id,
  });
}

export function useCreateControl() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateControlRequest) =>
      apiClient.compliance.createControl(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['compliance', 'controls'] });
    },
  });
}

export function useUpdateControl(id: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateControlRequest) =>
      apiClient.compliance.updateControl(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['compliance', 'controls'] });
      queryClient.invalidateQueries({ queryKey: ['compliance', 'controls', id] });
    },
  });
}

export function useDeleteControl() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => apiClient.compliance.deleteControl(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['compliance', 'controls'] });
    },
  });
}

// Mappings
export function useComplianceMappings(params?: ListMappingsRequest) {
  return useQuery({
    queryKey: ['compliance', 'mappings', params],
    queryFn: () => apiClient.compliance.listMappings(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useComplianceMapping(id: string) {
  return useQuery({
    queryKey: ['compliance', 'mappings', id],
    queryFn: () => apiClient.compliance.getMapping(id),
    enabled: !!id,
  });
}

export function useAssetMappings(assetId: string) {
  return useQuery({
    queryKey: ['compliance', 'mappings', 'asset', assetId],
    queryFn: () => apiClient.compliance.getAssetMappings(assetId),
    enabled: !!assetId,
  });
}

export function useCreateMapping() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateMappingRequest) =>
      apiClient.compliance.createMapping(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['compliance', 'mappings'] });
    },
  });
}

export function useUpdateMapping(id: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateMappingRequest) =>
      apiClient.compliance.updateMapping(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['compliance', 'mappings'] });
      queryClient.invalidateQueries({ queryKey: ['compliance', 'mappings', id] });
    },
  });
}

// Assessments
export function useComplianceAssessments(params?: ListAssessmentsRequest) {
  return useQuery({
    queryKey: ['compliance', 'assessments', params],
    queryFn: () => apiClient.compliance.listAssessments(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useComplianceAssessment(id: string) {
  return useQuery({
    queryKey: ['compliance', 'assessments', id],
    queryFn: () => apiClient.compliance.getAssessment(id),
    enabled: !!id,
  });
}

export function useCreateAssessment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateAssessmentRequest) =>
      apiClient.compliance.createAssessment(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['compliance', 'assessments'] });
    },
  });
}

export function useStartAssessment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => apiClient.compliance.startAssessment(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['compliance', 'assessments'] });
      queryClient.invalidateQueries({ queryKey: ['compliance', 'assessments', id] });
    },
  });
}

export function useCompleteAssessment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => apiClient.compliance.completeAssessment(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['compliance', 'assessments'] });
      queryClient.invalidateQueries({ queryKey: ['compliance', 'assessments', id] });
    },
  });
}

// Evidence
export function useComplianceEvidence(params?: ListEvidenceRequest) {
  return useQuery({
    queryKey: ['compliance', 'evidence', params],
    queryFn: () => apiClient.compliance.listEvidence(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useExpiringEvidence(days: number = 30) {
  return useQuery({
    queryKey: ['compliance', 'evidence', 'expiring', days],
    queryFn: () => apiClient.compliance.getExpiringEvidence(days),
    staleTime: 1 * 60 * 1000, // 1 minute
  });
}

export function useCreateEvidence() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateEvidenceRequest) =>
      apiClient.compliance.createEvidence(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['compliance', 'evidence'] });
    },
  });
}

// Gaps
export function useComplianceGaps(params?: ListGapsRequest) {
  return useQuery({
    queryKey: ['compliance', 'gaps', params],
    queryFn: () => apiClient.compliance.listGaps(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useCreateGap() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateGapRequest) =>
      apiClient.compliance.createGap(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['compliance', 'gaps'] });
    },
  });
}

export function useUpdateGap(id: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateGapRequest) =>
      apiClient.compliance.updateGap(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['compliance', 'gaps'] });
    },
  });
}

// Dashboard
export function useComplianceDashboard() {
  return useQuery({
    queryKey: ['compliance', 'dashboard'],
    queryFn: () => apiClient.compliance.getDashboard(),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}

export function useFrameworkDashboard(framework: ComplianceFramework) {
  return useQuery({
    queryKey: ['compliance', 'dashboard', framework],
    queryFn: () => apiClient.compliance.getFrameworkDashboard(framework),
    enabled: !!framework,
    staleTime: 2 * 60 * 1000,
  });
}
```

### E08 Scanning Hooks

```typescript
// Profiles
export function useScanProfiles(params?: ListProfilesRequest) {
  return useQuery({
    queryKey: ['scanning', 'profiles', params],
    queryFn: () => apiClient.scanning.listProfiles(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useScanProfile(id: string) {
  return useQuery({
    queryKey: ['scanning', 'profiles', id],
    queryFn: () => apiClient.scanning.getProfile(id),
    enabled: !!id,
  });
}

export function useCreateScanProfile() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateProfileRequest) =>
      apiClient.scanning.createProfile(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scanning', 'profiles'] });
    },
  });
}

export function useUpdateScanProfile(id: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateProfileRequest) =>
      apiClient.scanning.updateProfile(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scanning', 'profiles'] });
      queryClient.invalidateQueries({ queryKey: ['scanning', 'profiles', id] });
    },
  });
}

export function useValidateProfile() {
  return useMutation({
    mutationFn: (id: string) => apiClient.scanning.validateProfile(id),
  });
}

// Schedules
export function useScanSchedules(params?: ListSchedulesRequest) {
  return useQuery({
    queryKey: ['scanning', 'schedules', params],
    queryFn: () => apiClient.scanning.listSchedules(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useScanSchedule(id: string) {
  return useQuery({
    queryKey: ['scanning', 'schedules', id],
    queryFn: () => apiClient.scanning.getSchedule(id),
    enabled: !!id,
  });
}

export function useCreateScanSchedule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateScheduleRequest) =>
      apiClient.scanning.createSchedule(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scanning', 'schedules'] });
    },
  });
}

export function useToggleSchedule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, enabled }: { id: string; enabled: boolean }) =>
      enabled
        ? apiClient.scanning.enableSchedule(id)
        : apiClient.scanning.disableSchedule(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scanning', 'schedules'] });
    },
  });
}

// Jobs
export function useScanJobs(params?: ListJobsRequest) {
  return useQuery({
    queryKey: ['scanning', 'jobs', params],
    queryFn: () => apiClient.scanning.listJobs(params),
    staleTime: 1 * 60 * 1000, // 1 minute for active scans
    refetchInterval: (data) => {
      // Auto-refresh if any jobs are running
      const hasRunningJobs = data?.jobs?.some(
        (job) => job.status === ScanStatus.RUNNING || job.status === ScanStatus.QUEUED
      );
      return hasRunningJobs ? 10000 : false; // 10 seconds
    },
  });
}

export function useScanJob(id: string) {
  return useQuery({
    queryKey: ['scanning', 'jobs', id],
    queryFn: () => apiClient.scanning.getJob(id),
    enabled: !!id,
    refetchInterval: (data) => {
      // Auto-refresh if job is running
      const isRunning = data?.status === ScanStatus.RUNNING ||
                       data?.status === ScanStatus.QUEUED;
      return isRunning ? 5000 : false; // 5 seconds
    },
  });
}

export function useJobProgress(id: string) {
  return useQuery({
    queryKey: ['scanning', 'jobs', id, 'progress'],
    queryFn: () => apiClient.scanning.getJobProgress(id),
    enabled: !!id,
    refetchInterval: 5000, // 5 seconds
  });
}

export function useCreateScanJob() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateJobRequest) =>
      apiClient.scanning.createJob(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scanning', 'jobs'] });
    },
  });
}

export function useStartScanJob() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => apiClient.scanning.startJob(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['scanning', 'jobs'] });
      queryClient.invalidateQueries({ queryKey: ['scanning', 'jobs', id] });
    },
  });
}

export function usePauseScanJob() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => apiClient.scanning.pauseJob(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['scanning', 'jobs', id] });
    },
  });
}

export function useCancelScanJob() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => apiClient.scanning.cancelJob(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['scanning', 'jobs'] });
      queryClient.invalidateQueries({ queryKey: ['scanning', 'jobs', id] });
    },
  });
}

// Findings
export function useScanFindings(params?: ListFindingsRequest) {
  return useQuery({
    queryKey: ['scanning', 'findings', params],
    queryFn: () => apiClient.scanning.listFindings(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useScanFinding(id: string) {
  return useQuery({
    queryKey: ['scanning', 'findings', id],
    queryFn: () => apiClient.scanning.getFinding(id),
    enabled: !!id,
  });
}

export function useTrendingFindings() {
  return useQuery({
    queryKey: ['scanning', 'findings', 'trending'],
    queryFn: () => apiClient.scanning.getTrendingFindings(),
    staleTime: 5 * 60 * 1000,
  });
}

export function useUpdateFinding(id: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateFindingRequest) =>
      apiClient.scanning.updateFinding(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scanning', 'findings'] });
      queryClient.invalidateQueries({ queryKey: ['scanning', 'findings', id] });
    },
  });
}

export function useRemediateFinding() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => apiClient.scanning.remediateFinding(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scanning', 'findings'] });
    },
  });
}

// Dashboard
export function useScanningDashboard() {
  return useQuery({
    queryKey: ['scanning', 'dashboard'],
    queryFn: () => apiClient.scanning.getDashboard(),
    staleTime: 2 * 60 * 1000,
  });
}

export function useScanMetrics() {
  return useQuery({
    queryKey: ['scanning', 'metrics'],
    queryFn: () => apiClient.scanning.getMetrics(),
    staleTime: 2 * 60 * 1000,
  });
}
```

### E09 Alert Management Hooks

```typescript
// Alerts
export function useAlerts(params?: ListAlertsRequest) {
  return useQuery({
    queryKey: ['alerts', params],
    queryFn: () => apiClient.alerts.listAlerts(params),
    staleTime: 1 * 60 * 1000, // 1 minute for active alerts
    refetchInterval: (data) => {
      // Auto-refresh if there are new alerts
      const hasNewAlerts = data?.alerts?.some(
        (alert) => alert.status === AlertStatus.NEW
      );
      return hasNewAlerts ? 30000 : false; // 30 seconds
    },
  });
}

export function useAlert(id: string) {
  return useQuery({
    queryKey: ['alerts', id],
    queryFn: () => apiClient.alerts.getAlert(id),
    enabled: !!id,
  });
}

export function useCreateAlert() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateAlertRequest) =>
      apiClient.alerts.createAlert(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });
}

export function useUpdateAlert(id: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateAlertRequest) =>
      apiClient.alerts.updateAlert(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
      queryClient.invalidateQueries({ queryKey: ['alerts', id] });
    },
  });
}

export function useAcknowledgeAlert() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: AcknowledgeAlertRequest }) =>
      apiClient.alerts.acknowledgeAlert(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });
}

export function useResolveAlert() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: ResolveAlertRequest }) =>
      apiClient.alerts.resolveAlert(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });
}

export function useBulkAcknowledgeAlerts() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (alertIds: string[]) =>
      apiClient.alerts.bulkAcknowledge(alertIds),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });
}

export function useBulkResolveAlerts() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (alertIds: string[]) =>
      apiClient.alerts.bulkResolve(alertIds),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });
}

// Alert Rules
export function useAlertRules(params?: ListAlertRulesRequest) {
  return useQuery({
    queryKey: ['alerts', 'rules', params],
    queryFn: () => apiClient.alerts.listAlertRules(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useAlertRule(id: string) {
  return useQuery({
    queryKey: ['alerts', 'rules', id],
    queryFn: () => apiClient.alerts.getAlertRule(id),
    enabled: !!id,
  });
}

export function useCreateAlertRule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateAlertRuleRequest) =>
      apiClient.alerts.createAlertRule(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts', 'rules'] });
    },
  });
}

export function useUpdateAlertRule(id: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateAlertRuleRequest) =>
      apiClient.alerts.updateAlertRule(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts', 'rules'] });
      queryClient.invalidateQueries({ queryKey: ['alerts', 'rules', id] });
    },
  });
}

export function useToggleAlertRule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, enabled }: { id: string; enabled: boolean }) =>
      enabled
        ? apiClient.alerts.enableAlertRule(id)
        : apiClient.alerts.disableAlertRule(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts', 'rules'] });
    },
  });
}

export function useTestAlertRule() {
  return useMutation({
    mutationFn: (id: string) => apiClient.alerts.testAlertRule(id),
  });
}

// Notification Rules
export function useNotificationRules(params?: ListNotificationRulesRequest) {
  return useQuery({
    queryKey: ['alerts', 'notifications', params],
    queryFn: () => apiClient.alerts.listNotificationRules(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useNotificationRule(id: string) {
  return useQuery({
    queryKey: ['alerts', 'notifications', id],
    queryFn: () => apiClient.alerts.getNotificationRule(id),
    enabled: !!id,
  });
}

export function useCreateNotificationRule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateNotificationRuleRequest) =>
      apiClient.alerts.createNotificationRule(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts', 'notifications'] });
    },
  });
}

export function useTestNotification() {
  return useMutation({
    mutationFn: (id: string) => apiClient.alerts.testNotification(id),
  });
}

// Escalation Policies
export function useEscalationPolicies(params?: ListEscalationPoliciesRequest) {
  return useQuery({
    queryKey: ['alerts', 'escalations', params],
    queryFn: () => apiClient.alerts.listEscalationPolicies(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useEscalationPolicy(id: string) {
  return useQuery({
    queryKey: ['alerts', 'escalations', id],
    queryFn: () => apiClient.alerts.getEscalationPolicy(id),
    enabled: !!id,
  });
}

export function useCreateEscalationPolicy() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateEscalationPolicyRequest) =>
      apiClient.alerts.createEscalationPolicy(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts', 'escalations'] });
    },
  });
}

// Correlation
export function useAlertCorrelations(params?: ListCorrelationsRequest) {
  return useQuery({
    queryKey: ['alerts', 'correlations', params],
    queryFn: () => apiClient.alerts.listCorrelations(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useCorrelatedAlerts(correlationId: string) {
  return useQuery({
    queryKey: ['alerts', 'correlations', correlationId, 'matches'],
    queryFn: () => apiClient.alerts.getCorrelatedAlerts(correlationId),
    enabled: !!correlationId,
  });
}

// Statistics
export function useAlertStatistics(params: GetStatisticsRequest) {
  return useQuery({
    queryKey: ['alerts', 'statistics', params],
    queryFn: () => apiClient.alerts.getStatistics(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useTrendingAlerts() {
  return useQuery({
    queryKey: ['alerts', 'statistics', 'trending'],
    queryFn: () => apiClient.alerts.getTrendingAlerts(),
    staleTime: 5 * 60 * 1000,
  });
}

export function useMTTRMetrics() {
  return useQuery({
    queryKey: ['alerts', 'statistics', 'mttr'],
    queryFn: () => apiClient.alerts.getMTTRMetrics(),
    staleTime: 5 * 60 * 1000,
  });
}

export function useMTTAMetrics() {
  return useQuery({
    queryKey: ['alerts', 'statistics', 'mtta'],
    queryFn: () => apiClient.alerts.getMTTAMetrics(),
    staleTime: 5 * 60 * 1000,
  });
}
```

---

## API Client Examples

### E07 Compliance Client

```typescript
import axios from 'axios';
import { getAuthToken } from './auth';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000';

export const complianceClient = {
  // Controls
  async listControls(params?: ListControlsRequest): Promise<ListControlsResponse> {
    const { data } = await axios.get(`${BASE_URL}/api/v2/compliance/controls`, {
      params,
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
    return data;
  },

  async getControl(id: string): Promise<ComplianceControl> {
    const { data } = await axios.get(`${BASE_URL}/api/v2/compliance/controls/${id}`, {
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
    return data;
  },

  async createControl(payload: CreateControlRequest): Promise<ComplianceControl> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/compliance/controls`,
      payload,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async updateControl(id: string, payload: UpdateControlRequest): Promise<ComplianceControl> {
    const { data } = await axios.put(
      `${BASE_URL}/api/v2/compliance/controls/${id}`,
      payload,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async deleteControl(id: string): Promise<void> {
    await axios.delete(`${BASE_URL}/api/v2/compliance/controls/${id}`, {
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
  },

  // Mappings
  async listMappings(params?: ListMappingsRequest): Promise<ListMappingsResponse> {
    const { data } = await axios.get(`${BASE_URL}/api/v2/compliance/mappings`, {
      params,
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
    return data;
  },

  async getAssetMappings(assetId: string): Promise<ComplianceMapping[]> {
    const { data } = await axios.get(
      `${BASE_URL}/api/v2/compliance/mappings/asset/${assetId}`,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async createMapping(payload: CreateMappingRequest): Promise<ComplianceMapping> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/compliance/mappings`,
      payload,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  // Assessments
  async listAssessments(params?: ListAssessmentsRequest): Promise<ListAssessmentsResponse> {
    const { data } = await axios.get(`${BASE_URL}/api/v2/compliance/assessments`, {
      params,
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
    return data;
  },

  async startAssessment(id: string): Promise<ComplianceAssessment> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/compliance/assessments/${id}/start`,
      {},
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async completeAssessment(id: string): Promise<ComplianceAssessment> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/compliance/assessments/${id}/complete`,
      {},
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  // Dashboard
  async getDashboard(): Promise<any> {
    const { data } = await axios.get(`${BASE_URL}/api/v2/compliance/dashboard`, {
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
    return data;
  },

  async getFrameworkDashboard(framework: ComplianceFramework): Promise<any> {
    const { data } = await axios.get(
      `${BASE_URL}/api/v2/compliance/dashboard/framework/${framework}`,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },
};
```

### E08 Scanning Client

```typescript
export const scanningClient = {
  // Profiles
  async listProfiles(params?: ListProfilesRequest): Promise<ListProfilesResponse> {
    const { data } = await axios.get(`${BASE_URL}/api/v2/scanning/profiles`, {
      params,
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
    return data;
  },

  async createProfile(payload: CreateProfileRequest): Promise<ScanProfile> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/scanning/profiles`,
      payload,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async validateProfile(id: string): Promise<{ valid: boolean; errors?: string[] }> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/scanning/profiles/${id}/validate`,
      {},
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  // Jobs
  async listJobs(params?: ListJobsRequest): Promise<ListJobsResponse> {
    const { data } = await axios.get(`${BASE_URL}/api/v2/scanning/jobs`, {
      params,
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
    return data;
  },

  async createJob(payload: CreateJobRequest): Promise<ScanJob> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/scanning/jobs`,
      payload,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async startJob(id: string): Promise<ScanJob> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/scanning/jobs/${id}/start`,
      {},
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async pauseJob(id: string): Promise<ScanJob> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/scanning/jobs/${id}/pause`,
      {},
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async cancelJob(id: string): Promise<ScanJob> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/scanning/jobs/${id}/cancel`,
      {},
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async getJobProgress(id: string): Promise<{ progress: number; status: ScanStatus }> {
    const { data } = await axios.get(
      `${BASE_URL}/api/v2/scanning/jobs/${id}/progress`,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  // Findings
  async listFindings(params?: ListFindingsRequest): Promise<ListFindingsResponse> {
    const { data } = await axios.get(`${BASE_URL}/api/v2/scanning/findings`, {
      params,
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
    return data;
  },

  async updateFinding(id: string, payload: UpdateFindingRequest): Promise<ScanFinding> {
    const { data } = await axios.put(
      `${BASE_URL}/api/v2/scanning/findings/${id}`,
      payload,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async remediateFinding(id: string): Promise<ScanFinding> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/scanning/findings/${id}/remediate`,
      {},
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async getTrendingFindings(): Promise<ScanFinding[]> {
    const { data } = await axios.get(
      `${BASE_URL}/api/v2/scanning/findings/trending`,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },
};
```

### E09 Alerts Client

```typescript
export const alertsClient = {
  // Alerts
  async listAlerts(params?: ListAlertsRequest): Promise<ListAlertsResponse> {
    const { data } = await axios.get(`${BASE_URL}/api/v2/alerts`, {
      params,
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
    return data;
  },

  async createAlert(payload: CreateAlertRequest): Promise<Alert> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/alerts`,
      payload,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async acknowledgeAlert(id: string, payload: AcknowledgeAlertRequest): Promise<Alert> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/alerts/${id}/acknowledge`,
      payload,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async resolveAlert(id: string, payload: ResolveAlertRequest): Promise<Alert> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/alerts/${id}/resolve`,
      payload,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async bulkAcknowledge(alertIds: string[]): Promise<{ acknowledged: number }> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/alerts/bulk/acknowledge`,
      { alertIds },
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async bulkResolve(alertIds: string[]): Promise<{ resolved: number }> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/alerts/bulk/resolve`,
      { alertIds },
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  // Alert Rules
  async listAlertRules(params?: ListAlertRulesRequest): Promise<ListAlertRulesResponse> {
    const { data } = await axios.get(`${BASE_URL}/api/v2/alerts/rules`, {
      params,
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
    return data;
  },

  async createAlertRule(payload: CreateAlertRuleRequest): Promise<AlertRule> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/alerts/rules`,
      payload,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async enableAlertRule(id: string): Promise<AlertRule> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/alerts/rules/${id}/enable`,
      {},
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async disableAlertRule(id: string): Promise<AlertRule> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/alerts/rules/${id}/disable`,
      {},
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async testAlertRule(id: string): Promise<{ success: boolean; message: string }> {
    const { data } = await axios.post(
      `${BASE_URL}/api/v2/alerts/rules/${id}/test`,
      {},
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  // Statistics
  async getStatistics(params: GetStatisticsRequest): Promise<GetStatisticsResponse> {
    const { data } = await axios.get(`${BASE_URL}/api/v2/alerts/statistics`, {
      params,
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
    return data;
  },

  async getTrendingAlerts(): Promise<Alert[]> {
    const { data } = await axios.get(
      `${BASE_URL}/api/v2/alerts/statistics/trending`,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async getMTTRMetrics(): Promise<{ mttr: number; trend: string }> {
    const { data } = await axios.get(
      `${BASE_URL}/api/v2/alerts/statistics/mttr`,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },

  async getMTTAMetrics(): Promise<{ mtta: number; trend: string }> {
    const { data } = await axios.get(
      `${BASE_URL}/api/v2/alerts/statistics/mtta`,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    return data;
  },
};
```

---

## Integration Patterns

### Integration with Phase B2/B3 APIs

Phase B4 APIs are designed to integrate seamlessly with earlier phases:

#### Asset-Compliance Mapping
```typescript
// Link compliance controls to assets from Phase B2
const asset = await assetsClient.getAsset(assetId);
const mappings = await complianceClient.getAssetMappings(assetId);

// Create new mapping
await complianceClient.createMapping({
  controlId: 'NERC_CIP_005',
  assetId: asset.id,
  assetType: 'device',
  status: ComplianceStatus.COMPLIANT,
  implementationDetails: 'Firewall configured per NERC CIP-005 requirements',
  responsibleParty: 'security-team',
  reviewDate: new Date().toISOString(),
});
```

#### Scan Results to Alerts
```typescript
// Automatically create alerts from scan findings
const findings = await scanningClient.listFindings({
  jobId: scanJob.id,
  severity: FindingSeverity.CRITICAL,
});

for (const finding of findings.findings) {
  await alertsClient.createAlert({
    ruleId: 'auto-scan-critical',
    title: `Critical Vulnerability: ${finding.title}`,
    description: finding.description,
    severity: AlertSeverity.CRITICAL,
    category: AlertCategory.SECURITY,
    source: {
      type: 'scan',
      id: finding.id,
      name: finding.affectedComponent,
      metadata: { cveId: finding.cveId, cvssScore: finding.cvssScore },
    },
    context: {
      metric: 'vulnerability',
      value: finding.cvssScore,
      threshold: 9.0,
      additionalData: finding.vulnerability,
    },
  });
}
```

#### Compliance Evidence from Scans
```typescript
// Link scan reports as compliance evidence
const scanReport = await scanningClient.generateReport({
  jobId: scanJob.id,
  reportType: 'compliance',
  format: 'pdf',
});

await complianceClient.createEvidence({
  controlId: 'NERC_CIP_007',
  type: EvidenceType.SCAN_RESULT,
  title: `Vulnerability Scan - ${new Date().toLocaleDateString()}`,
  description: 'Automated vulnerability scan results',
  fileUrl: scanReport.report.reportUrl,
  expirationDate: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString(),
  tags: ['automated', 'vulnerability-scan', 'quarterly'],
});
```

#### Alert-Driven Compliance Gap Creation
```typescript
// Create compliance gaps from unresolved critical alerts
const criticalAlerts = await alertsClient.listAlerts({
  severity: AlertSeverity.CRITICAL,
  status: AlertStatus.NEW,
  category: AlertCategory.COMPLIANCE,
});

for (const alert of criticalAlerts.alerts) {
  await complianceClient.createGap({
    controlId: alert.source.metadata.controlId,
    description: `Compliance gap identified: ${alert.title}`,
    severity: 'critical',
    impact: alert.description,
    recommendedActions: ['Immediate remediation required', 'Document exception if needed'],
    estimatedEffort: 'high',
    targetDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
  });
}
```

---

## Qdrant Collections

Phase B4 introduces three new Qdrant collections for vector search and semantic analysis:

### Collection: ner11_compliance

**Purpose**: Store compliance controls, mappings, and assessment data for semantic search

**Schema**:
```typescript
{
  collection_name: "ner11_compliance",
  vectors: {
    size: 1536,  // OpenAI text-embedding-ada-002
    distance: "Cosine"
  },
  payload_schema: {
    customer_id: "keyword",
    document_type: "keyword",  // control, mapping, assessment, evidence, gap
    framework: "keyword",      // NERC_CIP, NIST_CSF, etc.
    control_id: "keyword",
    category: "keyword",
    severity: "keyword",
    status: "keyword",
    content: "text",
    metadata: "json"
  }
}
```

**Usage**:
```typescript
// Search for similar compliance controls
const results = await qdrantClient.search('ner11_compliance', {
  vector: await embedText(query),
  filter: {
    must: [
      { key: 'customer_id', match: { value: customerId } },
      { key: 'framework', match: { value: 'NERC_CIP' } },
    ],
  },
  limit: 10,
});
```

### Collection: ner11_scanning

**Purpose**: Store scan profiles, jobs, and findings for semantic analysis

**Schema**:
```typescript
{
  collection_name: "ner11_scanning",
  vectors: {
    size: 1536,
    distance: "Cosine"
  },
  payload_schema: {
    customer_id: "keyword",
    document_type: "keyword",  // profile, job, finding, report
    scan_type: "keyword",      // vulnerability, compliance, network, etc.
    severity: "keyword",
    status: "keyword",
    cve_id: "keyword",
    cvss_score: "float",
    content: "text",
    metadata: "json"
  }
}
```

**Usage**:
```typescript
// Find similar vulnerabilities
const results = await qdrantClient.search('ner11_scanning', {
  vector: await embedText(findingDescription),
  filter: {
    must: [
      { key: 'customer_id', match: { value: customerId } },
      { key: 'document_type', match: { value: 'finding' } },
      { key: 'severity', match: { value: 'critical' } },
    ],
  },
  limit: 5,
});
```

### Collection: ner11_alerts

**Purpose**: Store alerts, rules, and patterns for intelligent correlation

**Schema**:
```typescript
{
  collection_name: "ner11_alerts",
  vectors: {
    size: 1536,
    distance: "Cosine"
  },
  payload_schema: {
    customer_id: "keyword",
    document_type: "keyword",  // alert, rule, notification, escalation
    alert_category: "keyword",
    severity: "keyword",
    status: "keyword",
    source_type: "keyword",
    correlation_id: "keyword",
    content: "text",
    metadata: "json"
  }
}
```

**Usage**:
```typescript
// Find correlated alerts
const results = await qdrantClient.search('ner11_alerts', {
  vector: await embedText(alertDescription),
  filter: {
    must: [
      { key: 'customer_id', match: { value: customerId } },
      { key: 'document_type', match: { value: 'alert' } },
    ],
  },
  limit: 10,
});
```

---

## Performance Considerations

### Caching Strategy
- **Controls**: Cache for 5 minutes (infrequent updates)
- **Mappings**: Cache for 5 minutes
- **Assessments**: Cache for 5 minutes
- **Scan Profiles**: Cache for 5 minutes
- **Scan Jobs**: Cache for 1 minute, auto-refresh if running
- **Alerts**: Cache for 1 minute, auto-refresh if new alerts exist
- **Statistics**: Cache for 2-5 minutes

### Real-time Updates
- Scan jobs auto-refresh every 5-10 seconds when running
- Alerts auto-refresh every 30 seconds when new alerts exist
- WebSocket support for real-time alert notifications (optional)

### Pagination
- Default page size: 20 items
- Maximum page size: 100 items
- Use cursor-based pagination for large datasets

---

## Error Handling

All API endpoints follow consistent error response format:

```typescript
interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
    timestamp: string;
  };
}

// Common error codes
const ERROR_CODES = {
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  NOT_FOUND: 'NOT_FOUND',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  CONFLICT: 'CONFLICT',
  RATE_LIMIT_EXCEEDED: 'RATE_LIMIT_EXCEEDED',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
};
```

---

## Security Considerations

### Authentication
All API endpoints require Bearer token authentication:
```typescript
headers: {
  Authorization: `Bearer ${getAuthToken()}`
}
```

### Multi-Tenancy
All resources are automatically filtered by `customerId` from the authenticated user's token.

### Rate Limiting
- Standard endpoints: 1000 requests/hour per customer
- Scan execution: 100 scans/hour per customer
- Alert creation: 500 alerts/hour per customer

### Data Isolation
- Qdrant collections use customer-specific filtering
- All queries automatically include customer_id filter
- Cross-customer data access is prevented at the database level

---

## Next Steps

1. **Implementation**: Use these interfaces and hooks in your React components
2. **Testing**: Write integration tests for critical workflows
3. **Documentation**: Keep this reference updated as APIs evolve
4. **Monitoring**: Implement error tracking and performance monitoring

---

**Document Version**: 1.0.0
**Last Updated**: 2025-12-04
**Status**: PRODUCTION READY
