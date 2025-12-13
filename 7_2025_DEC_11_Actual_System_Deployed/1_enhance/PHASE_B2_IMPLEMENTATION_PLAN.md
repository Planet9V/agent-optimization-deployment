# Phase B2: Supply Chain Security Implementation Plan

**File**: PHASE_B2_IMPLEMENTATION_PLAN.md
**Created**: 2025-12-12 04:00:00 UTC
**Version**: v1.0.0
**Phase**: B2 - Supply Chain Security
**Total APIs**: 60 endpoints
**Duration**: 4-5 weeks (2-3 sprints)
**Priority**: 🔴 Critical
**Status**: ACTIVE

---

## 📋 Phase Overview

### Strategic Objectives
1. **Vendor Equipment Lifecycle Management**: Track 20-hop equipment chains from manufacturers to deployments
2. **SBOM Analysis Engine**: Parse, analyze, and track software components for vulnerability management
3. **Supply Chain Risk Assessment**: Identify risks in vendor dependencies and software components

### Business Value
- **Visibility**: Complete equipment and software component tracking
- **Risk Mitigation**: Early identification of vulnerable components
- **Compliance**: SBOM requirements for federal contracts (EO 14028)
- **Cost Savings**: Reduce incident response time by 60%

### Success Metrics
- Track 10,000+ vendor equipment instances
- Parse 1,000+ SBOMs across customer environments
- Identify vulnerable components within 24 hours of CVE publication
- Achieve <200ms response time for equipment queries

---

## 🏗️ Epic Breakdown

### Epic B2.1: E15 Vendor Equipment Lifecycle API
**Story Points**: 112 | **Duration**: 2 sprints | **APIs**: 28 endpoints

#### Sub-Epics
1. **Equipment Core CRUD** (8 APIs, 32 story points)
2. **Vendor Management** (6 APIs, 24 story points)
3. **Equipment Search & Analytics** (8 APIs, 32 story points)
4. **Equipment Relationships** (6 APIs, 24 story points)

### Epic B2.2: E03 SBOM Analysis Engine API
**Story Points**: 128 | **Duration**: 2-3 sprints | **APIs**: 32 endpoints

#### Sub-Epics
1. **SBOM Ingestion** (8 APIs, 32 story points)
2. **Component Analysis** (10 APIs, 40 story points)
3. **Vulnerability Matching** (8 APIs, 32 story points)
4. **SBOM Analytics** (6 APIs, 24 story points)

---

## 🎯 User Stories - Epic B2.1: Vendor Equipment

### Story B2.1.1: Equipment CRUD Operations
**Epic**: E15 Vendor Equipment | **Points**: 5 | **Priority**: Must Have

**As a** Security Analyst
**I want to** create, read, update, and delete equipment records
**So that** I can maintain an accurate inventory of deployed equipment

**Acceptance Criteria**:
- [ ] POST /api/v2/vendor-equipment/equipment creates equipment with required fields
- [ ] GET /api/v2/vendor-equipment/equipment/{id} retrieves equipment by ID
- [ ] PUT /api/v2/vendor-equipment/equipment/{id} updates equipment fields
- [ ] DELETE /api/v2/vendor-equipment/equipment/{id} soft-deletes equipment
- [ ] Validates required fields: model, serial_number, manufacturer, deployed_at
- [ ] Returns 400 for invalid data, 404 for not found, 200/201 on success

**Technical Specifications**:
```typescript
// Request Schema
interface CreateEquipmentRequest {
  model: string;
  serial_number: string;
  manufacturer_id: string;
  customer_id: string;
  deployed_at: string; // ISO 8601
  location?: string;
  status: 'active' | 'inactive' | 'decommissioned';
  metadata?: Record<string, any>;
}

// Response Schema
interface EquipmentResponse {
  id: string;
  model: string;
  serial_number: string;
  manufacturer: ManufacturerSummary;
  customer_id: string;
  deployed_at: string;
  location?: string;
  status: string;
  created_at: string;
  updated_at: string;
  vulnerability_count: number;
}

// Database Query (Neo4j)
CREATE (e:Equipment {
  id: randomUUID(),
  model: $model,
  serial_number: $serial_number,
  customer_id: $customer_id,
  deployed_at: datetime($deployed_at),
  status: $status,
  created_at: datetime(),
  updated_at: datetime()
})
WITH e
MATCH (m:Manufacturer {id: $manufacturer_id})
CREATE (e)-[:MANUFACTURED_BY]->(m)
RETURN e, m
```

**Testing Requirements**:
- Unit tests: CRUD operations, validation logic
- Integration tests: Database persistence, relationship creation
- API contract tests: OpenAPI schema validation

**Dependencies**:
- Neo4j schema with Equipment and Manufacturer nodes
- Clerk authentication middleware
- Customer isolation via X-Customer-ID header

**Story Points Breakdown**:
- Backend API implementation: 2 points
- Database queries & optimization: 1 point
- Testing & validation: 1 point
- Documentation: 1 point

---

### Story B2.1.2: Bulk Equipment Import
**Epic**: E15 Vendor Equipment | **Points**: 8 | **Priority**: Must Have

**As a** Security Administrator
**I want to** import equipment from CSV/Excel files
**So that** I can onboard existing equipment inventories efficiently

**Acceptance Criteria**:
- [ ] POST /api/v2/vendor-equipment/equipment/bulk-import accepts CSV/XLSX files
- [ ] Validates file format and required columns
- [ ] Processes up to 10,000 equipment records in single import
- [ ] Returns validation errors for invalid rows
- [ ] Creates background job for large imports (>1000 records)
- [ ] Provides import status via GET /api/v2/vendor-equipment/equipment/import-jobs/{id}

**Technical Specifications**:
```typescript
// Request (multipart/form-data)
interface BulkImportRequest {
  file: File; // CSV or XLSX
  import_mode: 'create' | 'update' | 'upsert';
  customer_id: string;
}

// Response
interface BulkImportResponse {
  job_id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  total_rows: number;
  processed_rows: number;
  successful: number;
  failed: number;
  errors: Array<{
    row: number;
    field: string;
    message: string;
  }>;
  estimated_completion?: string;
}

// CSV Format
model,serial_number,manufacturer_name,deployed_at,location,status
Cisco 2960X,ABC123456,Cisco Systems,2024-01-15,Building A,active
Fortinet FG-200E,DEF789012,Fortinet,2024-02-20,Data Center,active
```

**Database Operations**:
```cypher
// Bulk create with UNWIND
UNWIND $equipment_batch AS eq
CREATE (e:Equipment {
  id: randomUUID(),
  model: eq.model,
  serial_number: eq.serial_number,
  customer_id: $customer_id,
  deployed_at: datetime(eq.deployed_at),
  location: eq.location,
  status: eq.status,
  created_at: datetime(),
  updated_at: datetime()
})
WITH e, eq
MATCH (m:Manufacturer {name: eq.manufacturer_name})
CREATE (e)-[:MANUFACTURED_BY]->(m)
RETURN count(e) as created_count
```

**Testing Requirements**:
- Unit tests: File parsing, validation logic, batch processing
- Integration tests: Background job creation, status updates
- Load tests: 10,000 record import performance

**Dependencies**:
- File upload handler (multipart/form-data)
- CSV/XLSX parser library (papaparse, xlsx)
- Background job queue (Bull or similar)
- Redis for job status tracking

**Story Points Breakdown**:
- File parsing implementation: 2 points
- Batch processing & validation: 2 points
- Background job integration: 2 points
- Testing & error handling: 1 point
- Documentation: 1 point

---

### Story B2.1.3: Equipment Search with Advanced Filters
**Epic**: E15 Vendor Equipment | **Points**: 5 | **Priority**: Must Have

**As a** Security Analyst
**I want to** search equipment by multiple criteria
**So that** I can quickly find equipment matching specific conditions

**Acceptance Criteria**:
- [ ] GET /api/v2/vendor-equipment/equipment/search supports query parameters
- [ ] Filters: manufacturer, model, status, deployed_date_range, location, has_vulnerabilities
- [ ] Pagination: cursor-based with page_size up to 100
- [ ] Sorting: by deployed_at, model, vulnerability_count (asc/desc)
- [ ] Returns total_count for pagination UI
- [ ] Response time <200ms for queries returning <1000 records

**Technical Specifications**:
```typescript
// Request Query Parameters
interface EquipmentSearchParams {
  manufacturer_id?: string;
  model?: string; // partial match
  status?: 'active' | 'inactive' | 'decommissioned';
  deployed_after?: string; // ISO 8601
  deployed_before?: string;
  location?: string; // partial match
  has_vulnerabilities?: boolean;
  cursor?: string; // for pagination
  page_size?: number; // default 20, max 100
  sort_by?: 'deployed_at' | 'model' | 'vulnerability_count';
  sort_order?: 'asc' | 'desc';
}

// Response
interface EquipmentSearchResponse {
  equipment: EquipmentResponse[];
  pagination: {
    total_count: number;
    page_size: number;
    next_cursor?: string;
    previous_cursor?: string;
  };
  filters_applied: EquipmentSearchParams;
}
```

**Database Query**:
```cypher
MATCH (e:Equipment)-[:MANUFACTURED_BY]->(m:Manufacturer)
WHERE e.customer_id = $customer_id
  AND ($manufacturer_id IS NULL OR m.id = $manufacturer_id)
  AND ($model IS NULL OR e.model CONTAINS $model)
  AND ($status IS NULL OR e.status = $status)
  AND ($deployed_after IS NULL OR e.deployed_at >= datetime($deployed_after))
  AND ($deployed_before IS NULL OR e.deployed_at <= datetime($deployed_before))
  AND ($location IS NULL OR e.location CONTAINS $location)
OPTIONAL MATCH (e)-[:HAS_VULNERABILITY]->(v:Vulnerability)
WITH e, m, count(v) as vuln_count
WHERE ($has_vulnerabilities IS NULL OR
       ($has_vulnerabilities = true AND vuln_count > 0) OR
       ($has_vulnerabilities = false AND vuln_count = 0))
RETURN e, m, vuln_count
ORDER BY
  CASE $sort_by
    WHEN 'deployed_at' THEN e.deployed_at
    WHEN 'model' THEN e.model
    WHEN 'vulnerability_count' THEN vuln_count
  END
SKIP $offset
LIMIT $page_size
```

**Testing Requirements**:
- Unit tests: Query parameter validation, pagination logic
- Integration tests: All filter combinations, sorting, pagination
- Performance tests: Query response time with 10,000+ equipment records

**Story Points Breakdown**:
- Query parameter parsing: 1 point
- Neo4j query optimization: 2 points
- Pagination & sorting logic: 1 point
- Testing: 1 point

---

### Story B2.1.4: Equipment Vulnerability Tracking
**Epic**: E15 Vendor Equipment | **Points**: 8 | **Priority**: Must Have

**As a** Security Analyst
**I want to** see all vulnerabilities affecting specific equipment
**So that** I can prioritize remediation efforts

**Acceptance Criteria**:
- [ ] GET /api/v2/vendor-equipment/equipment/{id}/vulnerabilities returns CVEs
- [ ] Includes severity, CVSS score, exploitability, remediation status
- [ ] Filters by severity (critical, high, medium, low), status (open, in_progress, resolved)
- [ ] Shows affected software components from SBOM
- [ ] Provides remediation recommendations
- [ ] Links to vendor security advisories

**Technical Specifications**:
```typescript
// Response
interface EquipmentVulnerabilitiesResponse {
  equipment_id: string;
  equipment_summary: {
    model: string;
    manufacturer: string;
    deployed_at: string;
  };
  vulnerability_summary: {
    critical: number;
    high: number;
    medium: number;
    low: number;
    total: number;
  };
  vulnerabilities: Array<{
    cve_id: string;
    title: string;
    severity: string;
    cvss_score: number;
    published_date: string;
    exploitability: 'high' | 'medium' | 'low' | 'none';
    remediation_status: 'open' | 'in_progress' | 'resolved' | 'mitigated';
    affected_components: Array<{
      name: string;
      version: string;
      package_url: string;
    }>;
    remediation_options: Array<{
      type: 'patch' | 'upgrade' | 'workaround' | 'configuration';
      description: string;
      vendor_advisory_url?: string;
    }>;
  }>;
}
```

**Database Query**:
```cypher
MATCH (e:Equipment {id: $equipment_id})
MATCH (e)-[:RUNS_SOFTWARE]->(c:Component)
MATCH (c)-[:HAS_VULNERABILITY]->(v:Vulnerability)
OPTIONAL MATCH (v)-[:REMEDIATED_BY]->(r:Remediation)
RETURN e, v, c, r
ORDER BY v.cvss_score DESC
```

**Testing Requirements**:
- Unit tests: Severity aggregation, status filtering
- Integration tests: Multi-hop traversal (equipment → components → vulnerabilities)
- Performance tests: Query optimization for equipment with 100+ components

**Story Points Breakdown**:
- Multi-hop query implementation: 3 points
- Aggregation & filtering logic: 2 points
- Remediation matching: 2 points
- Testing: 1 point

---

### Story B2.1.5: Vendor Management
**Epic**: E15 Vendor Equipment | **Points**: 5 | **Priority**: Must Have

**As a** Procurement Manager
**I want to** manage vendor information and risk ratings
**So that** I can make informed purchasing decisions

**Acceptance Criteria**:
- [ ] POST /api/v2/vendor-equipment/vendors creates vendor with risk rating
- [ ] GET /api/v2/vendor-equipment/vendors lists vendors with equipment counts
- [ ] PUT /api/v2/vendor-equipment/vendors/{id} updates vendor details
- [ ] GET /api/v2/vendor-equipment/vendors/{id}/risk-profile calculates risk score
- [ ] Risk factors: vulnerability count, patch latency, EOL products
- [ ] Links to vendor security advisories and contact information

**Technical Specifications**:
```typescript
interface CreateVendorRequest {
  name: string;
  website?: string;
  contact_email?: string;
  security_advisory_url?: string;
  risk_rating?: 'low' | 'medium' | 'high' | 'critical';
  notes?: string;
}

interface VendorRiskProfile {
  vendor_id: string;
  vendor_name: string;
  risk_score: number; // 0-100
  risk_factors: {
    total_equipment: number;
    equipment_with_vulnerabilities: number;
    critical_vulnerabilities: number;
    average_patch_latency_days: number;
    eol_equipment_count: number;
    security_incidents_last_year: number;
  };
  risk_rating: 'low' | 'medium' | 'high' | 'critical';
  recommendations: string[];
}
```

**Database Query**:
```cypher
MATCH (v:Manufacturer {id: $vendor_id})
MATCH (e:Equipment)-[:MANUFACTURED_BY]->(v)
OPTIONAL MATCH (e)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
WITH v, count(DISTINCT e) as total_equipment,
     count(DISTINCT CASE WHEN vuln IS NOT NULL THEN e END) as vuln_equipment,
     count(DISTINCT CASE WHEN vuln.severity = 'CRITICAL' THEN vuln END) as critical_vulns
RETURN v, total_equipment, vuln_equipment, critical_vulns
```

**Story Points Breakdown**:
- Vendor CRUD operations: 2 points
- Risk calculation logic: 2 points
- Testing & documentation: 1 point

---

### Story B2.1.6: Equipment Lifecycle Timeline
**Epic**: E15 Vendor Equipment | **Points**: 5 | **Priority**: Should Have

**As a** Asset Manager
**I want to** view equipment lifecycle events in timeline
**So that** I can track installation, updates, and decommissioning

**Acceptance Criteria**:
- [ ] GET /api/v2/vendor-equipment/equipment/{id}/timeline returns chronological events
- [ ] Events: deployed, updated, vulnerability_detected, patched, decommissioned
- [ ] Includes event metadata, user who performed action, timestamps
- [ ] Supports filtering by event_type and date_range
- [ ] Paginated results with cursor-based navigation

**Technical Specifications**:
```typescript
interface EquipmentTimelineEvent {
  id: string;
  equipment_id: string;
  event_type: 'deployed' | 'updated' | 'vulnerability_detected' |
              'patched' | 'configuration_changed' | 'decommissioned';
  timestamp: string;
  user_id?: string;
  user_name?: string;
  description: string;
  metadata: Record<string, any>;
  related_entities?: Array<{
    type: 'vulnerability' | 'patch' | 'configuration';
    id: string;
    name: string;
  }>;
}

interface EquipmentTimelineResponse {
  equipment_id: string;
  events: EquipmentTimelineEvent[];
  pagination: {
    total_count: number;
    next_cursor?: string;
  };
}
```

**Database Query**:
```cypher
MATCH (e:Equipment {id: $equipment_id})-[r:HAS_EVENT]->(evt:Event)
WHERE ($event_type IS NULL OR evt.type = $event_type)
  AND ($start_date IS NULL OR evt.timestamp >= datetime($start_date))
  AND ($end_date IS NULL OR evt.timestamp <= datetime($end_date))
OPTIONAL MATCH (evt)-[:RELATED_TO]->(related)
RETURN e, evt, collect(related) as related_entities
ORDER BY evt.timestamp DESC
SKIP $offset
LIMIT $page_size
```

**Story Points Breakdown**:
- Event tracking implementation: 2 points
- Timeline query & pagination: 2 points
- Testing: 1 point

---

## 🎯 User Stories - Epic B2.2: SBOM Analysis

### Story B2.2.1: SBOM Upload and Parsing
**Epic**: E03 SBOM Analysis | **Points**: 8 | **Priority**: Must Have

**As a** Security Engineer
**I want to** upload SBOM files in multiple formats
**So that** I can analyze software components for vulnerabilities

**Acceptance Criteria**:
- [ ] POST /api/v2/sbom/sboms accepts SBOM files (CycloneDX, SPDX)
- [ ] Supports JSON and XML formats
- [ ] Validates SBOM structure against schema
- [ ] Extracts components, dependencies, licenses
- [ ] Associates SBOM with equipment or application
- [ ] Returns parsing errors for invalid SBOMs

**Technical Specifications**:
```typescript
interface UploadSBOMRequest {
  file: File; // CycloneDX or SPDX format
  format: 'cyclonedx' | 'spdx';
  content_type: 'json' | 'xml';
  equipment_id?: string;
  application_name?: string;
  customer_id: string;
}

interface SBOMParseResponse {
  sbom_id: string;
  format: string;
  parsed_at: string;
  component_count: number;
  dependency_count: number;
  license_count: number;
  validation_errors: Array<{
    field: string;
    message: string;
  }>;
  components_summary: {
    total: number;
    with_known_vulnerabilities: number;
    with_license_issues: number;
  };
}

// CycloneDX Schema (simplified)
interface CycloneDX {
  bomFormat: 'CycloneDX';
  specVersion: string;
  serialNumber: string;
  version: number;
  metadata: {
    timestamp: string;
    component: {
      type: string;
      name: string;
      version: string;
    };
  };
  components: Array<{
    type: 'library' | 'framework' | 'application' | 'container';
    'bom-ref': string;
    name: string;
    version: string;
    purl?: string; // Package URL
    licenses?: Array<{
      license: {
        id: string;
        name: string;
      };
    }>;
  }>;
  dependencies?: Array<{
    ref: string;
    dependsOn: string[];
  }>;
}
```

**Database Operations**:
```cypher
// Create SBOM node
CREATE (s:SBOM {
  id: randomUUID(),
  format: $format,
  serial_number: $serial_number,
  version: $version,
  uploaded_at: datetime(),
  customer_id: $customer_id
})

// Create component nodes
UNWIND $components AS comp
CREATE (c:Component {
  id: randomUUID(),
  bom_ref: comp.bom_ref,
  type: comp.type,
  name: comp.name,
  version: comp.version,
  purl: comp.purl,
  created_at: datetime()
})
CREATE (s)-[:CONTAINS_COMPONENT]->(c)

// Create dependencies
UNWIND $dependencies AS dep
MATCH (parent:Component {bom_ref: dep.ref})
MATCH (child:Component {bom_ref: dep.dependsOn})
CREATE (parent)-[:DEPENDS_ON]->(child)
```

**Testing Requirements**:
- Unit tests: CycloneDX parser, SPDX parser, validation
- Integration tests: File upload, database persistence
- Test fixtures: Valid/invalid SBOM files

**Dependencies**:
- SBOM parsing libraries (@cyclonedx/sbom-utils, spdx-tools)
- File upload middleware
- XML parser for XML-format SBOMs

**Story Points Breakdown**:
- SBOM parser implementation: 3 points
- Component extraction logic: 2 points
- Database persistence: 2 points
- Testing: 1 point

---

### Story B2.2.2: Component Vulnerability Matching
**Epic**: E03 SBOM Analysis | **Points**: 13 | **Priority**: Must Have

**As a** Security Analyst
**I want to** automatically match SBOM components to known vulnerabilities
**So that** I can identify vulnerable software quickly

**Acceptance Criteria**:
- [ ] Automatic matching on SBOM upload via background job
- [ ] Matches components using Package URL (purl)
- [ ] Matches using CPE (Common Platform Enumeration) when available
- [ ] Fuzzy matching for components without purl/CPE
- [ ] GET /api/v2/sbom/sboms/{id}/vulnerabilities returns matched CVEs
- [ ] Includes severity, CVSS, exploitability, patch availability
- [ ] Updates automatically when new CVEs are published

**Technical Specifications**:
```typescript
interface ComponentVulnerabilityMatch {
  component: {
    id: string;
    name: string;
    version: string;
    purl?: string;
    cpe?: string;
  };
  vulnerabilities: Array<{
    cve_id: string;
    title: string;
    severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
    cvss_score: number;
    cvss_vector: string;
    published_date: string;
    modified_date: string;
    exploitability: 'high' | 'medium' | 'low' | 'none';
    exploits_available: boolean;
    patch_available: boolean;
    patch_version?: string;
    affected_versions: string[]; // version ranges
    references: string[];
  }>;
  match_confidence: 'exact' | 'high' | 'medium' | 'low';
  match_method: 'purl' | 'cpe' | 'name_version' | 'fuzzy';
}

interface SBOMVulnerabilityReport {
  sbom_id: string;
  total_components: number;
  vulnerable_components: number;
  total_vulnerabilities: number;
  severity_breakdown: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  components_with_vulnerabilities: ComponentVulnerabilityMatch[];
  generated_at: string;
}
```

**Vulnerability Matching Logic**:
```typescript
async function matchComponentVulnerabilities(component: Component): Promise<Vulnerability[]> {
  let vulnerabilities: Vulnerability[] = [];

  // 1. Exact match via Package URL (purl)
  if (component.purl) {
    vulnerabilities = await db.query(`
      MATCH (c:Component {purl: $purl})-[:HAS_VULNERABILITY]->(v:Vulnerability)
      RETURN v
    `, { purl: component.purl });

    if (vulnerabilities.length > 0) {
      return vulnerabilities;
    }
  }

  // 2. CPE match
  if (component.cpe) {
    vulnerabilities = await db.query(`
      MATCH (c:Component)-[:HAS_CPE]->(cpe:CPE {uri: $cpe})
      MATCH (cpe)-[:HAS_VULNERABILITY]->(v:Vulnerability)
      WHERE v.affected_versions CONTAINS $version
      RETURN v
    `, { cpe: component.cpe, version: component.version });

    if (vulnerabilities.length > 0) {
      return vulnerabilities;
    }
  }

  // 3. Name + version match
  vulnerabilities = await db.query(`
    MATCH (c:Component {name: $name})
    MATCH (c)-[:HAS_VULNERABILITY]->(v:Vulnerability)
    WHERE any(range IN v.affected_versions WHERE $version MATCHES range)
    RETURN v
  `, { name: component.name, version: component.version });

  // 4. Fuzzy matching (Levenshtein distance for similar names)
  if (vulnerabilities.length === 0) {
    vulnerabilities = await fuzzyMatchVulnerabilities(component);
  }

  return vulnerabilities;
}
```

**Database Query**:
```cypher
// Get all components with vulnerabilities
MATCH (s:SBOM {id: $sbom_id})-[:CONTAINS_COMPONENT]->(c:Component)
OPTIONAL MATCH (c)-[:HAS_VULNERABILITY]->(v:Vulnerability)
RETURN c, collect(v) as vulnerabilities
ORDER BY v.cvss_score DESC
```

**Testing Requirements**:
- Unit tests: Each matching method (purl, CPE, name/version, fuzzy)
- Integration tests: Background job execution, database updates
- Performance tests: Matching 1000+ components in <30 seconds

**Dependencies**:
- NVD CVE database integration
- Background job queue (Bull/BullMQ)
- Version comparison library (semver)

**Story Points Breakdown**:
- Matching algorithm implementation: 5 points
- Background job integration: 3 points
- Performance optimization: 3 points
- Testing: 2 points

---

### Story B2.2.3: SBOM Comparison and Drift Detection
**Epic**: E03 SBOM Analysis | **Points**: 8 | **Priority**: Should Have

**As a** DevOps Engineer
**I want to** compare SBOMs across versions
**So that** I can detect unauthorized component changes

**Acceptance Criteria**:
- [ ] GET /api/v2/sbom/sboms/{id}/compare?with={other_id} compares two SBOMs
- [ ] Shows added, removed, updated components
- [ ] Highlights security implications (new vulnerabilities, license changes)
- [ ] Supports comparing SBOM snapshots over time
- [ ] Provides diff visualization data for frontend

**Technical Specifications**:
```typescript
interface SBOMComparisonRequest {
  sbom_id_1: string; // baseline
  sbom_id_2: string; // comparison
}

interface SBOMComparisonResponse {
  comparison_id: string;
  baseline_sbom: {
    id: string;
    version: string;
    uploaded_at: string;
    component_count: number;
  };
  comparison_sbom: {
    id: string;
    version: string;
    uploaded_at: string;
    component_count: number;
  };
  changes: {
    components_added: Array<{
      name: string;
      version: string;
      has_vulnerabilities: boolean;
      vulnerability_count?: number;
    }>;
    components_removed: Array<{
      name: string;
      version: string;
    }>;
    components_updated: Array<{
      name: string;
      version_from: string;
      version_to: string;
      severity_change?: 'increased' | 'decreased' | 'unchanged';
      new_vulnerabilities: number;
      resolved_vulnerabilities: number;
    }>;
  };
  security_impact: {
    new_critical_vulnerabilities: number;
    new_high_vulnerabilities: number;
    resolved_vulnerabilities: number;
    risk_score_change: number; // +/- percentage
  };
  license_impact: {
    new_restrictive_licenses: string[];
    license_conflicts: string[];
  };
}
```

**Database Query**:
```cypher
// Find added components
MATCH (s2:SBOM {id: $sbom_id_2})-[:CONTAINS_COMPONENT]->(c2:Component)
WHERE NOT EXISTS {
  MATCH (s1:SBOM {id: $sbom_id_1})-[:CONTAINS_COMPONENT]->(:Component {name: c2.name})
}
OPTIONAL MATCH (c2)-[:HAS_VULNERABILITY]->(v:Vulnerability)
RETURN c2, count(v) as vuln_count

// Find removed components
MATCH (s1:SBOM {id: $sbom_id_1})-[:CONTAINS_COMPONENT]->(c1:Component)
WHERE NOT EXISTS {
  MATCH (s2:SBOM {id: $sbom_id_2})-[:CONTAINS_COMPONENT]->(:Component {name: c1.name})
}
RETURN c1

// Find updated components
MATCH (s1:SBOM {id: $sbom_id_1})-[:CONTAINS_COMPONENT]->(c1:Component)
MATCH (s2:SBOM {id: $sbom_id_2})-[:CONTAINS_COMPONENT]->(c2:Component {name: c1.name})
WHERE c1.version <> c2.version
OPTIONAL MATCH (c1)-[:HAS_VULNERABILITY]->(v1:Vulnerability)
OPTIONAL MATCH (c2)-[:HAS_VULNERABILITY]->(v2:Vulnerability)
RETURN c1, c2, count(v1) as old_vulns, count(v2) as new_vulns
```

**Story Points Breakdown**:
- Comparison algorithm: 3 points
- Security impact calculation: 2 points
- Database queries optimization: 2 points
- Testing: 1 point

---

### Story B2.2.4: SBOM Analytics Dashboard
**Epic**: E03 SBOM Analysis | **Points**: 5 | **Priority**: Should Have

**As a** CISO
**I want to** view SBOM analytics across my organization
**So that** I can understand software component risks

**Acceptance Criteria**:
- [ ] GET /api/v2/sbom/analytics/dashboard returns organization-wide metrics
- [ ] Metrics: total SBOMs, total components, vulnerability distribution
- [ ] Top vulnerable components across all SBOMs
- [ ] License compliance overview
- [ ] Trend data (vulnerability count over time)
- [ ] Filtering by customer, application, date range

**Technical Specifications**:
```typescript
interface SBOMAnalyticsDashboard {
  organization_summary: {
    total_sboms: number;
    total_unique_components: number;
    total_vulnerabilities: number;
    sboms_with_critical_vulns: number;
    average_vulns_per_sbom: number;
  };
  vulnerability_distribution: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  top_vulnerable_components: Array<{
    component_name: string;
    version: string;
    occurrence_count: number; // used in N SBOMs
    vulnerability_count: number;
    highest_cvss: number;
  }>;
  license_compliance: {
    total_licenses: number;
    permissive: number;
    restrictive: number;
    unknown: number;
    conflicting_licenses: string[];
  };
  trends: {
    sbom_uploads_last_30_days: Array<{
      date: string;
      count: number;
    }>;
    vulnerability_count_trend: Array<{
      date: string;
      total: number;
      critical: number;
      high: number;
    }>;
  };
}
```

**Database Query**:
```cypher
// Organization summary
MATCH (s:SBOM {customer_id: $customer_id})
MATCH (s)-[:CONTAINS_COMPONENT]->(c:Component)
OPTIONAL MATCH (c)-[:HAS_VULNERABILITY]->(v:Vulnerability)
RETURN count(DISTINCT s) as total_sboms,
       count(DISTINCT c) as total_components,
       count(DISTINCT v) as total_vulnerabilities,
       avg(v.cvss_score) as avg_cvss

// Top vulnerable components
MATCH (c:Component)-[:HAS_VULNERABILITY]->(v:Vulnerability)
WITH c, count(v) as vuln_count, max(v.cvss_score) as max_cvss
ORDER BY vuln_count DESC
LIMIT 10
RETURN c.name, c.version, vuln_count, max_cvss
```

**Story Points Breakdown**:
- Aggregation queries: 2 points
- Trend calculation: 1 point
- API implementation: 1 point
- Testing: 1 point

---

## 📅 Sprint Planning

### Sprint 1: Equipment Core & Vendor Management
**Duration**: 2 weeks | **Capacity**: 96 points | **Allocated**: 89 points

**Goals**:
- Complete equipment CRUD operations
- Implement vendor management
- Enable equipment search functionality

**Stories**:
1. B2.1.1: Equipment CRUD (5 points)
2. B2.1.2: Bulk Equipment Import (8 points)
3. B2.1.3: Equipment Search (5 points)
4. B2.1.5: Vendor Management (5 points)
5. B2.2.1: SBOM Upload & Parsing (8 points)
6. Database schema setup (13 points)
7. Authentication middleware (8 points)
8. API documentation setup (5 points)
9. CI/CD pipeline configuration (13 points)
10. Integration testing framework (13 points)
11. Sprint retrospective & planning (6 points)

**Deliverables**:
- [ ] 5 equipment APIs operational
- [ ] 6 vendor APIs operational
- [ ] 1 SBOM upload API operational
- [ ] Database schema deployed
- [ ] CI/CD pipeline active
- [ ] Test coverage ≥80%

---

### Sprint 2: Equipment Analytics & SBOM Vulnerability Matching
**Duration**: 2 weeks | **Capacity**: 96 points | **Allocated**: 92 points

**Goals**:
- Complete equipment vulnerability tracking
- Implement component vulnerability matching
- Enable SBOM comparison

**Stories**:
1. B2.1.4: Equipment Vulnerability Tracking (8 points)
2. B2.1.6: Equipment Lifecycle Timeline (5 points)
3. B2.2.2: Component Vulnerability Matching (13 points)
4. B2.2.3: SBOM Comparison (8 points)
5. B2.2.4: SBOM Analytics Dashboard (5 points)
6. Background job queue setup (13 points)
7. Performance optimization (13 points)
8. Load testing (8 points)
9. Security audit (8 points)
10. Documentation completion (8 points)
11. Sprint demo & retrospective (3 points)

**Deliverables**:
- [ ] All 28 equipment APIs complete
- [ ] All 32 SBOM APIs complete
- [ ] Vulnerability matching operational
- [ ] SBOM comparison working
- [ ] Analytics dashboard data available
- [ ] Performance targets met (<200ms p95)
- [ ] Security scan passed

---

### Sprint 3: Polish, Integration & Launch Prep
**Duration**: 1 week | **Capacity**: 48 points | **Allocated**: 47 points

**Goals**:
- Bug fixes and polish
- End-to-end integration testing
- Production deployment preparation

**Stories**:
1. Bug fixes from sprint 2 (13 points)
2. End-to-end integration tests (13 points)
3. Production deployment scripts (8 points)
4. Monitoring & alerting setup (8 points)
5. User documentation (5 points)

**Deliverables**:
- [ ] All critical bugs resolved
- [ ] Integration tests passing
- [ ] Production deployment ready
- [ ] Monitoring dashboards configured
- [ ] User documentation complete
- [ ] Phase B2 launch ready

---

## 🧪 Testing Strategy

### Unit Testing
- **Target**: ≥85% code coverage
- **Framework**: Jest for TypeScript, pytest for Python
- **Focus Areas**: Business logic, validation, data transformations

### Integration Testing
- **Target**: All critical paths covered
- **Framework**: Supertest for API testing, Cypress for E2E
- **Focus Areas**: Database operations, multi-hop queries, authentication

### Performance Testing
- **Tool**: k6 or Artillery
- **Targets**:
  - API response time: <200ms p95
  - SBOM parsing: <10 seconds for 1000-component SBOM
  - Bulk import: <30 seconds for 1000 equipment records
  - Vulnerability matching: <30 seconds for 500 components

### Security Testing
- **Static Analysis**: SonarQube, Snyk
- **Dependency Scanning**: npm audit, Dependabot
- **API Security**: OWASP ZAP scans

---

## 📊 Success Metrics

### Technical Metrics
- [ ] **Code Coverage**: ≥85% for all APIs
- [ ] **API Response Time**: <200ms p95 for all endpoints
- [ ] **Database Query Performance**: <100ms for simple queries, <500ms for complex analytics
- [ ] **SBOM Parsing Time**: <10 seconds per SBOM (up to 1000 components)
- [ ] **Vulnerability Matching Accuracy**: ≥95% for components with purl/CPE
- [ ] **Uptime**: ≥99.9% during beta period

### Business Metrics
- [ ] **Equipment Tracking**: 10,000+ equipment instances tracked
- [ ] **SBOM Analysis**: 1,000+ SBOMs analyzed
- [ ] **Vulnerability Detection**: 10,000+ component vulnerabilities identified
- [ ] **User Adoption**: 5 pilot customers successfully onboarded
- [ ] **Time to Value**: <2 hours from signup to first vulnerability report

---

## 🚀 Deployment Plan

### Pre-Deployment Checklist
- [ ] All APIs implemented and tested
- [ ] Database migrations prepared
- [ ] Environment variables configured
- [ ] Monitoring dashboards created
- [ ] Runbooks for common issues
- [ ] Rollback plan documented

### Deployment Stages
1. **Development**: Continuous deployment from feature branches
2. **Staging**: Deploy to staging after sprint completion
3. **Beta**: Deploy to production with feature flags (5 customers)
4. **General Availability**: Full production launch after 2 weeks beta

### Rollback Strategy
- **Automated Rollback**: If error rate >5% in 5 minutes
- **Manual Rollback**: Database migration issues, data corruption
- **Rollback Time**: <15 minutes to previous stable version

---

## 🔗 Dependencies

### External Dependencies
- **NVD CVE Database**: For vulnerability data
- **CycloneDX/SPDX Libraries**: For SBOM parsing
- **Clerk**: For authentication
- **Neo4j**: Graph database
- **Qdrant**: Vector database (future semantic search)

### Internal Dependencies
- **Neo4j Schema**: Equipment, Component, Vulnerability nodes
- **Background Job Queue**: Bull/BullMQ for async processing
- **File Upload Service**: Multipart form data handling
- **Notification Service**: Alert stakeholders of critical vulnerabilities

---

## 📝 Next Steps

1. **Review and approve** this implementation plan
2. **Assign stories** to sprint backlog
3. **Set up development environment** for all team members
4. **Kick off Sprint 1** with sprint planning meeting
5. **Begin implementation** of Phase B2 APIs

---

**Status**: Ready for sprint planning
**Next Review**: After Sprint 1 (2 weeks)
**Owner**: Backend Team Lead
