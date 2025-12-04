# TASK SPECIFICATIONS - Option B MVP

**Project**: NER11 Gold Model Enhancement Roadmap
**Created**: 2025-12-03
**Last Updated**: 2025-12-04T03:25:00Z
**Version**: 1.0.1
**Status**: ACTIVE
**Strategy**: OPTION B - Balanced Foundation MVP

---

## Decision Record

| Item | Value |
|------|-------|
| Selected Strategy | **OPTION B - Balanced Foundation MVP** |
| Decision Date | 2025-12-04T03:15:00Z |
| MVP Duration | 62 days |
| MVP Enhancements | 6 |
| Deferred Enhancements | 13 |

---

## Table of Contents

### MVP Phase B1: Structural Foundation (Days 1-20)
1. [CUSTOMER_LABELS: Multi-Tenant Isolation](#customer_labels-multi-tenant-isolation) 🔴 **MVP**
2. [E07: IEC 62443 Safety Integration](#e07-iec-62443-safety-integration) 🔴 **MVP**

### MVP Phase B2: Supply Chain (Days 21-44)
3. [E15: Vendor Equipment Tracking](#e15-vendor-equipment-tracking) 🟡 **MVP**
4. [E03: SBOM Vulnerability Analysis](#e03-sbom-vulnerability-analysis) 🟡 **MVP**

### MVP Phase B3: Prioritization (Days 45-62)
5. [E10: Economic Impact Modeling](#e10-economic-impact-modeling) 🟡 **MVP**
6. [E12: NOW/NEXT/NEVER Prioritization](#e12-nownextnever-prioritization) 🔴 **MVP**

### Deferred Phase D1: Safety & Reliability (Post-MVP)
7. [E08: RAMS Reliability Analysis](#e08-rams-reliability-analysis) ⏸️ **DEFERRED**
8. [E09: Hazard & FMEA Integration](#e09-hazard--fmea-integration) ⏸️ **DEFERRED**

### Deferred Phase D2: Advanced Analysis (Post-MVP)
9. [E11: Psychohistory Demographics](#e11-psychohistory-demographics) ⏸️ **DEFERRED**
10. [E13: Attack Path Modeling](#e13-attack-path-modeling) ⏸️ **DEFERRED**

### Deferred Phase D3: Psychometric Core (Post-MVP)
11. [E19: Organizational Blind Spots](#e19-organizational-blind-spots) ⏸️ **DEFERRED**
12. [E20: Personality-Team Fit Analysis](#e20-personality-team-fit-analysis) ⏸️ **DEFERRED**
13. [E21: Transcript Psychometric NER](#e21-transcript-psychometric-ner) ⏸️ **DEFERRED**
14. [E24: Cognitive Dissonance Detection](#e24-cognitive-dissonance-detection) ⏸️ **DEFERRED**
15. [E25: Threat Actor Personality Profiling](#e25-threat-actor-personality-profiling) ⏸️ **DEFERRED**

### Deferred Phase D4: Experimental Psychohistory (Post-MVP)
16. [E17: Lacanian Dyad Analysis](#e17-lacanian-dyad-analysis) 🧪 **EXPERIMENTAL**
17. [E18: Triad Group Dynamics](#e18-triad-group-dynamics) 🧪 **EXPERIMENTAL**
18. [E22: Seldon Crisis Prediction](#e22-seldon-crisis-prediction) 🧪 **EXPERIMENTAL**
19. [E23: Population Event Forecasting](#e23-population-event-forecasting) 🧪 **EXPERIMENTAL**

---

## MVP Enhancement Summary

| Order | ID | Name | Phase | Days | Priority | Status |
|-------|-----|------|-------|------|----------|--------|
| 1 | CUSTOMER_LABELS | Multi-Tenant Isolation | B1 | 5 | CRITICAL | NOT STARTED |
| 2 | E07 | IEC 62443 Industrial Safety | B1 | 15 | CRITICAL | NOT STARTED |
| 3 | E15 | Vendor Equipment Tracking | B2 | 12 | HIGH | NOT STARTED |
| 4 | E03 | SBOM Dependency Analysis | B2 | 12 | HIGH | NOT STARTED |
| 5 | E10 | Economic Impact Analysis | B3 | 10 | HIGH | NOT STARTED |
| 6 | E12 | NOW/NEXT/NEVER Prioritization | B3 | 8 | CRITICAL | NOT STARTED |

---

## MVP Phase B1: Structural Foundation

### CUSTOMER_LABELS: Multi-Tenant Isolation

🔴 **MVP ENHANCEMENT - Phase B1 - Order 1**

**Enhancement ID**: CUSTOMER_LABELS
**Name**: Multi-Tenant Isolation
**MVP Phase**: B1 - Structural Foundation
**MVP Order**: 1 of 6
**Priority**: CRITICAL
**ICE Score**: 9.5
**Estimated Days**: 5 days (Days 1-5 of MVP)

---

#### 1. Objective Statement

Implement a comprehensive multi-tenant security framework that enables isolation and access control for customer-specific data within the NER11 Gold Model, ensuring complete data segregation while maintaining query performance and system scalability.

---

#### 2. Acceptance Criteria

**GIVEN** a Neo4j database with mixed customer data
**WHEN** a user queries the system
**THEN** they should only access data labeled with their customer ID

**GIVEN** a new customer entity is created
**WHEN** the entity is stored in Neo4j
**THEN** it must be automatically labeled with the correct customer_id property

**GIVEN** a query across multiple entity types
**WHEN** the query executes with customer context
**THEN** all returned entities must belong to the specified customer

**GIVEN** an admin user with cross-customer access
**WHEN** they query the system
**THEN** they should see aggregated data across all customers with proper isolation markers

**GIVEN** a customer deletion request
**WHEN** the deletion is executed
**THEN** all entities with matching customer_id must be removed with zero data leakage

**GIVEN** a performance benchmark on customer-filtered queries
**WHEN** compared to unfiltered queries
**THEN** performance degradation must not exceed 10%

**GIVEN** a security audit log
**WHEN** customer data is accessed
**THEN** all access must be logged with customer_id, user, timestamp, and operation

---

#### 3. Technical Requirements

**Neo4j Schema Changes:**
```cypher
// Add customer_id property to all entity types
CREATE CONSTRAINT customer_id_exists IF NOT EXISTS
FOR (n:Entity) REQUIRE n.customer_id IS NOT NULL;

// Create index for customer filtering
CREATE INDEX customer_id_index IF NOT EXISTS
FOR (n:Entity) ON (n.customer_id);

// Customer node definition
CREATE (c:Customer {
  customer_id: string,
  name: string,
  created_at: datetime,
  active: boolean,
  tier: string,  // 'free', 'standard', 'enterprise'
  metadata: map
});

// Add customer_id to all existing entity types
MATCH (n) WHERE n:Vulnerability OR n:Asset OR n:Threat OR n:CVE
SET n.customer_id = COALESCE(n.customer_id, 'default_customer');
```

**API Endpoints:**

| Method | Path | Payload | Response |
|--------|------|---------|----------|
| POST | `/api/v1/customers` | `{name, tier, metadata}` | `{customer_id, ...}` |
| GET | `/api/v1/customers/:id` | - | `{customer_id, name, stats}` |
| GET | `/api/v1/customers/:id/entities` | `?type=Vulnerability` | `[entities]` |
| DELETE | `/api/v1/customers/:id` | - | `{deleted_count}` |
| GET | `/api/v1/auth/context` | - | `{customer_id, permissions}` |

**Frontend Components:**
- CustomerSelector dropdown component
- CustomerContext provider (React Context)
- ProtectedRoute component with customer authorization
- CustomerDashboard with statistics

**Data Integrations:**
- Neo4j: Primary data store with customer labels
- Qdrant: Embeddings tagged with customer_id metadata
- Authentication service: JWT tokens with customer_id claim

---

#### 4. Dependencies

**Enhancement Dependencies:**
- None (Foundation enhancement)

**External Dependencies:**
- Neo4j 5.x with APOC library
- JWT authentication service
- Redis for session management (optional)

**Internal Dependencies:**
- NER11 Gold Model entity schema
- Existing API authentication layer
- Qdrant vector database

---

#### 5. Data Sources

**Internal:**
- Neo4j: All entity types (Vulnerability, Asset, Threat, CVE, etc.)
- Qdrant: Vector embeddings with customer metadata
- NER11 Gold Model: 189,932 existing entities requiring retroactive labeling

**External:**
- None (Internal infrastructure enhancement)

**Migration Data:**
- Existing entities: 189,932 nodes requiring `customer_id` assignment
- Default customer ID: `default_customer` for legacy data

---

#### 6. Implementation Steps

1. **Schema Design**: Define Customer node schema and customer_id property standards
2. **Constraint Creation**: Add NOT NULL constraint for customer_id on all entity types
3. **Index Creation**: Create composite indexes for (customer_id, entity_type) queries
4. **Migration Script**: Write Cypher script to add customer_id to existing 189k entities
5. **Migration Execution**: Execute migration with progress tracking and rollback capability
6. **API Middleware**: Implement CustomerContextMiddleware to extract customer_id from JWT
7. **Query Interceptor**: Add automatic customer_id filtering to all Neo4j queries
8. **Customer Management API**: Build CRUD endpoints for Customer entity management
9. **Frontend Context**: Implement React CustomerContext provider
10. **Protected Routes**: Add customer authorization to all API routes
11. **Qdrant Integration**: Update vector search to filter by customer_id metadata
12. **Audit Logging**: Implement access logging with customer_id tracking
13. **Performance Testing**: Benchmark query performance with customer filtering
14. **Security Audit**: Verify data isolation across customer boundaries
15. **Documentation**: Create multi-tenant architecture documentation

---

#### 7. Test Requirements

**Unit Tests:**
```javascript
// Test customer_id constraint enforcement
test('Entity creation without customer_id should fail', async () => {
  await expect(createEntity({type: 'Vulnerability'}))
    .rejects.toThrow('customer_id is required');
});

// Test customer_id filtering
test('Query should only return entities for specified customer', async () => {
  const results = await queryEntities({customer_id: 'cust_123'});
  expect(results.every(e => e.customer_id === 'cust_123')).toBe(true);
});

// Test cross-customer isolation
test('Customer A should not access Customer B data', async () => {
  const results = await queryEntities({customer_id: 'cust_A'});
  expect(results.some(e => e.customer_id === 'cust_B')).toBe(false);
});
```

**Integration Tests:**
- Test full request lifecycle with JWT customer_id extraction
- Test Qdrant vector search with customer filtering
- Test customer deletion cascade across Neo4j and Qdrant
- Test admin cross-customer queries

**Acceptance Tests:**
- Create 3 test customers with 100 entities each
- Verify complete data isolation across customers
- Verify performance < 10% degradation
- Verify audit logs capture all customer access

**Minimum Coverage**: 80% for multi-tenant logic

---

#### 8. Audit Checklist

- [ ] All 189,932 existing entities have valid customer_id
- [ ] Neo4j constraints prevent customer_id omission
- [ ] Performance benchmarks show < 10% degradation
- [ ] Security testing confirms zero cross-customer data leakage
- [ ] Audit logs capture 100% of customer data access
- [ ] Documentation covers multi-tenant architecture and migration
- [ ] Admin users can query across customers with proper authorization

---

#### 9. Rollback Plan

**Pre-Migration Backup:**
```bash
# Backup Neo4j database
neo4j-admin dump --database=neo4j --to=/backup/pre-multitenant.dump

# Backup Qdrant collections
curl -X GET "http://qdrant:6333/collections/ner11/snapshots"
```

**Rollback Steps:**
1. Stop application services
2. Restore Neo4j from backup dump
3. Restore Qdrant collections from snapshots
4. Remove customer_id indexes and constraints
5. Restart services with previous API version
6. Verify data integrity and query functionality

**Rollback Time**: < 30 minutes

---

#### 10. Estimated Story Points

**Complexity Factors:**
- Schema migration: 3 points
- API middleware: 2 points
- Query interceptors: 3 points
- Frontend integration: 2 points
- Testing & validation: 3 points

**Total**: 13 story points (Moderate complexity, critical infrastructure)

---

### E07: IEC 62443 Safety Integration

🔴 **MVP ENHANCEMENT - Phase B1 - Order 2**

**Enhancement ID**: E07
**Name**: IEC 62443 Industrial Safety Standards
**MVP Phase**: B1 - Structural Foundation
**MVP Order**: 2 of 6
**Priority**: CRITICAL
**ICE Score**: 8.7
**Estimated Days**: 15 days (Days 6-20 of MVP)

---

#### 1. Objective Statement

Integrate IEC 62443 industrial control system (ICS) security standards into the NER11 Gold Model to enable safety-critical vulnerability assessment, security level classification, and compliance mapping for operational technology (OT) environments.

---

#### 2. Acceptance Criteria

**GIVEN** a CVE affecting industrial control systems
**WHEN** the vulnerability is analyzed
**THEN** it must be mapped to IEC 62443 security levels (SL 1-4) and foundational requirements (FR 1-7)

**GIVEN** an asset tagged as industrial equipment
**WHEN** the asset is assessed
**THEN** it must have a target security level and current compliance status

**GIVEN** a vulnerability with IEC 62443 classification
**WHEN** a risk assessment is performed
**THEN** safety impact scores must consider operational disruption and human safety

**GIVEN** a query for ICS-specific vulnerabilities
**WHEN** filtering by IEC 62443 domains
**THEN** results must include zone, conduit, and security level metadata

**GIVEN** a compliance report generation request
**WHEN** targeting IEC 62443 framework
**THEN** the report must show gap analysis across FR 1-7 categories

**GIVEN** a SCADA system asset
**WHEN** linked vulnerabilities are analyzed
**THEN** cascading safety impact across zones must be calculated

**GIVEN** performance benchmarks for ICS vulnerability queries
**WHEN** compared to standard CVE queries
**THEN** query time must not exceed 2x standard query latency

---

#### 3. Technical Requirements

**Neo4j Schema Changes:**
```cypher
// IEC 62443 Security Level node
CREATE (sl:SecurityLevel {
  level: int,  // 1-4
  name: string,  // 'SL-1: Protection against casual or coincidental violation'
  description: string,
  requirements: [string]
});

// Foundational Requirement node
CREATE (fr:FoundationalRequirement {
  fr_id: string,  // 'FR-1' to 'FR-7'
  name: string,  // 'Identification and Authentication Control'
  category: string,
  controls: [string]
});

// Zone and Conduit nodes for network segmentation
CREATE (z:Zone {
  zone_id: string,
  name: string,
  security_level: int,
  criticality: string,  // 'safety-critical', 'business-critical', 'non-critical'
  assets: [string]
});

CREATE (con:Conduit {
  conduit_id: string,
  name: string,
  from_zone: string,
  to_zone: string,
  allowed_protocols: [string],
  security_level: int
});

// Add ICS properties to Asset node
MATCH (a:Asset)
SET a.is_ics = boolean,
    a.target_security_level = int,
    a.current_security_level = int,
    a.zone_id = string,
    a.ics_type = string;  // 'PLC', 'SCADA', 'HMI', 'DCS', 'RTU', 'IED'

// Add IEC 62443 classification to Vulnerability
MATCH (v:Vulnerability)
SET v.iec62443_fr = [string],  // Foundational Requirements affected
    v.iec62443_sl_required = int,  // Minimum SL required to mitigate
    v.safety_impact = string,  // 'none', 'low', 'medium', 'high', 'critical'
    v.operational_impact = string;

// Relationships
CREATE (a:Asset)-[:IN_ZONE]->(z:Zone);
CREATE (z1:Zone)-[:CONNECTED_VIA]->(con:Conduit)-[:CONNECTED_TO]->(z2:Zone);
CREATE (v:Vulnerability)-[:VIOLATES_FR]->(fr:FoundationalRequirement);
CREATE (a:Asset)-[:REQUIRES_SL]->(sl:SecurityLevel);
```

**API Endpoints:**

| Method | Path | Payload | Response |
|--------|------|---------|----------|
| GET | `/api/v1/iec62443/security-levels` | - | `[{level, name, requirements}]` |
| GET | `/api/v1/iec62443/foundational-requirements` | - | `[{fr_id, name, controls}]` |
| POST | `/api/v1/iec62443/zones` | `{name, security_level, criticality}` | `{zone_id, ...}` |
| GET | `/api/v1/iec62443/zones/:id/vulnerabilities` | - | `[vulnerabilities]` |
| POST | `/api/v1/iec62443/compliance-report` | `{asset_id, target_sl}` | `{gaps: [...], compliance_score}` |
| GET | `/api/v1/iec62443/cascading-impact/:vuln_id` | - | `{affected_zones, safety_risk}` |
| PUT | `/api/v1/assets/:id/ics-metadata` | `{is_ics, ics_type, target_sl}` | `{updated}` |

**Frontend Components:**
- IEC62443Dashboard with security level overview
- ZoneVisualization component (network diagram)
- ComplianceReportGenerator
- SafetyImpactMatrix heatmap

**Data Integrations:**
- Neo4j: IEC 62443 taxonomy and asset classification
- NVD API: CVE data enrichment with ICS tags
- ICS-CERT Advisories: Industrial vulnerability data

---

#### 4. Dependencies

**Enhancement Dependencies:**
- E01: Customer Labels (Multi-Tenant) - Required for customer-specific ICS assets

**External Dependencies:**
- ICS-CERT Advisory Database
- NVD CVE feeds with ICS/OT tags
- IEC 62443 standard documentation (parts 1-4)

**Internal Dependencies:**
- Neo4j graph database
- NER11 Gold Model entity schema
- Asset management system

---

#### 5. Data Sources

**Internal:**
- Neo4j: Existing Asset and Vulnerability nodes
- NER11 Gold Model: 189,932 entities for ICS classification

**External:**
- **ICS-CERT Advisories**: https://www.cisa.gov/ics-advisories
  - ~500 annual advisories for ICS vulnerabilities
- **NVD CVE API**: https://services.nvd.nist.gov/rest/json/cves/2.0
  - Filter by CPE names containing "siemens", "schneider", "rockwell", "abb", etc.
- **IEC 62443 Standard**: Official standard documentation for FR and SL definitions
- **MITRE ATT&CK for ICS**: https://attack.mitre.org/matrices/ics/

**Specific Datasets:**
- ICS-CERT Advisory JSON feed (daily updates)
- NVD CPE dictionary for ICS vendors
- IEC 62443-3-3 control requirements mapping

---

#### 6. Implementation Steps

1. **Standards Research**: Analyze IEC 62443 parts 1-4 for schema requirements
2. **Schema Design**: Define SecurityLevel, FoundationalRequirement, Zone, Conduit nodes
3. **Schema Implementation**: Execute Cypher DDL for IEC 62443 entities
4. **Asset Classification**: Script to tag existing assets with ICS metadata (is_ics, ics_type)
5. **ICS-CERT Integration**: Build ETL pipeline for ICS-CERT advisory ingestion
6. **CVE Enrichment**: Enhance NVD CVE data with ICS tags and IEC 62443 mappings
7. **FR Mapping Logic**: Implement vulnerability-to-FR mapping algorithm
8. **Security Level Assessment**: Build SL calculation based on asset criticality and vulnerabilities
9. **Zone Modeling**: Implement zone and conduit relationship management
10. **Cascading Impact Analysis**: Build graph algorithm for cross-zone safety impact
11. **Compliance Report Generator**: Implement gap analysis across FR 1-7
12. **API Development**: Build 7 IEC 62443-specific endpoints
13. **Frontend Dashboard**: Create IEC 62443 visualization components
14. **Testing**: ICS vulnerability scenarios and compliance report validation
15. **Documentation**: Create IEC 62443 integration guide and API documentation

---

#### 7. Test Requirements

**Unit Tests:**
```javascript
// Test ICS asset classification
test('Asset tagged as PLC should have ICS metadata', async () => {
  const asset = await createAsset({name: 'Siemens S7-1200', ics_type: 'PLC'});
  expect(asset.is_ics).toBe(true);
  expect(asset.target_security_level).toBeGreaterThan(0);
});

// Test FR mapping
test('CVE-2023-1234 should map to FR-2 and FR-5', async () => {
  const vuln = await getVulnerability('CVE-2023-1234');
  expect(vuln.iec62443_fr).toContain('FR-2');
  expect(vuln.iec62443_fr).toContain('FR-5');
});

// Test cascading impact calculation
test('Vulnerability in Zone A should calculate safety impact on connected zones', async () => {
  const impact = await calculateCascadingImpact('vuln_123');
  expect(impact.affected_zones).toContain('Zone B');
  expect(impact.safety_risk).toBe('high');
});
```

**Integration Tests:**
- Test ICS-CERT advisory ETL pipeline with sample data
- Test compliance report generation for SCADA system with 20 vulnerabilities
- Test zone visualization with 5 zones and 10 conduits
- Test security level upgrade recommendations

**Acceptance Tests:**
- Classify 100 ICS assets with target security levels
- Map 50 ICS vulnerabilities to FR categories
- Generate compliance report showing FR-1 to FR-7 gaps
- Verify cascading impact across 3-zone network

**Minimum Coverage**: 80% for IEC 62443 logic

---

#### 8. Audit Checklist

- [ ] All ICS assets have target_security_level assigned
- [ ] All ICS vulnerabilities mapped to FR categories
- [ ] Zone and conduit relationships accurately represent network segmentation
- [ ] Cascading impact algorithm validated with real-world SCADA scenarios
- [ ] Compliance reports align with IEC 62443-3-3 control requirements
- [ ] ICS-CERT advisory pipeline processes daily updates
- [ ] Documentation covers IEC 62443 integration and compliance workflows

---

#### 9. Rollback Plan

**Pre-Implementation Backup:**
```bash
# Backup Neo4j before schema changes
neo4j-admin dump --database=neo4j --to=/backup/pre-iec62443.dump

# Backup ICS asset classifications
MATCH (a:Asset) WHERE a.is_ics = true
RETURN a.asset_id, a.ics_type, a.target_security_level
// Export to CSV
```

**Rollback Steps:**
1. Stop application and ETL pipelines
2. Restore Neo4j from backup dump
3. Remove IEC 62443-specific indexes and constraints
4. Remove ICS-CERT advisory integration
5. Revert API endpoints to previous version
6. Clear frontend dashboard components

**Rollback Time**: < 45 minutes

---

#### 10. Estimated Story Points

**Complexity Factors:**
- Standards research: 3 points
- Schema design: 3 points
- ICS-CERT integration: 5 points
- Cascading impact algorithm: 5 points
- Compliance reporting: 3 points
- Frontend visualization: 3 points
- Testing & validation: 5 points

**Total**: 27 story points (High complexity, specialized domain knowledge required)

---

---

## MVP Phase B2: Supply Chain

### E15: Vendor Equipment Tracking

🟡 **MVP ENHANCEMENT - Phase B2 - Order 3**

**Enhancement ID**: E15
**Name**: Vendor Equipment Lifecycle Management
**MVP Phase**: B2 - Supply Chain
**MVP Order**: 3 of 6
**Priority**: HIGH
**ICE Score**: 7.0
**Estimated Days**: 12 days (Days 21-32 of MVP)

---

#### 1. Objective Statement

Implement comprehensive vendor equipment tracking and lifecycle management within the NER11 Gold Model, enabling end-of-life (EOL) monitoring, vendor risk assessment, supply chain vulnerability tracking, and maintenance scheduling for critical infrastructure assets.

---

#### 2. Acceptance Criteria

**GIVEN** an asset from a known vendor
**WHEN** the asset is registered
**THEN** it must be linked to a Vendor node with complete metadata (name, risk score, support status)

**GIVEN** a vendor with multiple equipment models
**WHEN** querying vendor risk
**THEN** the system must return aggregated vulnerability counts and average CVSS scores

**GIVEN** an equipment model with an EOL date
**WHEN** the current date is within 180 days of EOL
**THEN** the system must flag the asset as "approaching EOL" with maintenance recommendations

**GIVEN** a supply chain vulnerability (e.g., SolarWinds)
**WHEN** the vulnerability is identified
**THEN** all assets from the affected vendor must be automatically flagged

**GIVEN** a vendor with multiple support contracts
**WHEN** a support contract expires
**THEN** affected assets must be marked with "support_status: expired" and escalated

**GIVEN** a query for critical infrastructure vendors
**WHEN** filtering by risk score > 7.0
**THEN** results must include vendor risk factors, open CVEs, and affected asset counts

**GIVEN** a maintenance schedule for 50 assets
**WHEN** the schedule is generated
**THEN** it must prioritize by EOL proximity, vulnerability count, and criticality

---

#### 3. Technical Requirements

**Neo4j Schema Changes:**
```cypher
// Vendor node
CREATE (v:Vendor {
  vendor_id: string,
  name: string,
  risk_score: float,  // 0.0-10.0
  support_status: string,  // 'active', 'limited', 'eol', 'deprecated'
  country: string,
  industry_focus: [string],  // ['ICS', 'IT', 'Medical', 'IoT']
  supply_chain_tier: int,  // 1=direct, 2=indirect, 3=tertiary
  last_incident_date: date,
  total_cves: int,
  avg_cvss_score: float,
  metadata: map
});

// Equipment model node
CREATE (em:EquipmentModel {
  model_id: string,
  vendor_id: string,
  model_name: string,
  product_line: string,
  release_date: date,
  eol_date: date,
  eos_date: date,  // End of Support
  current_version: string,
  supported_versions: [string],
  maintenance_schedule: string,  // 'monthly', 'quarterly', 'annual'
  criticality: string,  // 'low', 'medium', 'high', 'critical'
  metadata: map
});

// Support contract node
CREATE (sc:SupportContract {
  contract_id: string,
  vendor_id: string,
  customer_id: string,
  start_date: date,
  end_date: date,
  service_level: string,  // 'basic', 'standard', 'premium', 'enterprise'
  response_time_sla: int,  // hours
  coverage: [string],  // ['security_patches', 'firmware_updates', '24/7_support']
  status: string,  // 'active', 'expired', 'pending_renewal'
  annual_cost: float
});

// Supply chain incident node
CREATE (sci:SupplyChainIncident {
  incident_id: string,
  vendor_id: string,
  incident_type: string,  // 'breach', 'vulnerability', 'outage', 'bankruptcy'
  severity: string,
  description: string,
  discovery_date: date,
  resolution_date: date,
  affected_products: [string],
  cve_ids: [string]
});

// Add vendor tracking to Asset node
MATCH (a:Asset)
SET a.vendor_id = string,
    a.model_id = string,
    a.purchase_date = date,
    a.warranty_end_date = date,
    a.maintenance_due_date = date,
    a.eol_status = string;  // 'active', 'approaching_eol', 'eol', 'eos'

// Relationships
CREATE (a:Asset)-[:MANUFACTURED_BY]->(v:Vendor);
CREATE (a:Asset)-[:MODEL_OF]->(em:EquipmentModel);
CREATE (em:EquipmentModel)-[:PRODUCED_BY]->(v:Vendor);
CREATE (v:Vendor)-[:HAS_CONTRACT]->(sc:SupportContract);
CREATE (v:Vendor)-[:INVOLVED_IN]->(sci:SupplyChainIncident);
CREATE (a:Asset)-[:COVERED_BY]->(sc:SupportContract);
```

**API Endpoints:**

| Method | Path | Payload | Response |
|--------|------|---------|----------|
| POST | `/api/v1/vendors` | `{name, country, industry_focus}` | `{vendor_id, ...}` |
| GET | `/api/v1/vendors/:id` | - | `{vendor_id, risk_score, total_cves, assets}` |
| GET | `/api/v1/vendors/:id/risk-assessment` | - | `{risk_factors, vulnerabilities, incidents}` |
| POST | `/api/v1/equipment-models` | `{vendor_id, model_name, eol_date}` | `{model_id, ...}` |
| GET | `/api/v1/equipment-models/:id/lifecycle` | - | `{release_date, eol_date, eos_date, status}` |
| GET | `/api/v1/vendors/:id/supply-chain-incidents` | - | `[incidents]` |
| POST | `/api/v1/support-contracts` | `{vendor_id, customer_id, end_date, sla}` | `{contract_id, ...}` |
| GET | `/api/v1/support-contracts/expiring` | `?days=90` | `[contracts]` |
| GET | `/api/v1/assets/eol-approaching` | `?days=180` | `[assets]` |
| POST | `/api/v1/maintenance/schedule` | `{asset_ids, priority}` | `{schedule: [...]}` |

**Frontend Components:**
- VendorRiskDashboard with risk score heatmap
- EOLTracker component with timeline visualization
- SupplyChainIncidentTimeline
- MaintenanceScheduler calendar view
- SupportContractManager

**Data Integrations:**
- Neo4j: Vendor, EquipmentModel, SupportContract nodes
- CVE databases: Vendor-specific vulnerability tracking
- Asset management system: Equipment inventory
- Support ticket system: Maintenance history

---

#### 4. Dependencies

**Enhancement Dependencies:**
- E01: Customer Labels (Multi-Tenant) - Required for customer-specific vendor tracking

**External Dependencies:**
- Vendor EOL databases (e.g., endoflife.date API)
- CVE feeds filtered by vendor CPE names
- Supply chain incident databases (e.g., SecurityScorecard)

**Internal Dependencies:**
- Neo4j graph database
- NER11 Gold Model Asset entities
- Asset inventory system

---

#### 5. Data Sources

**Internal:**
- Neo4j: Existing Asset nodes requiring vendor linkage
- NER11 Gold Model: 189,932 entities for vendor classification

**External:**
- **endoflife.date API**: https://endoflife.date/api/
  - EOL dates for 300+ products (Cisco, Juniper, Microsoft, etc.)
- **NVD CVE API**: https://services.nvd.nist.gov/rest/json/cves/2.0
  - Filter by vendor CPE names
- **SecurityScorecard Vendor API**: Vendor risk scores and supply chain incidents
- **Vendor support portals**: Cisco, Dell, HP, Lenovo, etc. (manual integration)

**Specific Datasets:**
- Vendor CPE dictionary from NVD
- Supply chain incident reports from CISA
- Asset inventory CSV exports from CMDB systems

---

#### 6. Implementation Steps

1. **Vendor Database Research**: Identify major vendors and risk scoring methodologies
2. **Schema Design**: Define Vendor, EquipmentModel, SupportContract, SupplyChainIncident nodes
3. **Schema Implementation**: Execute Cypher DDL for vendor tracking entities
4. **EOL Data Integration**: Build ETL pipeline for endoflife.date API
5. **Vendor-CVE Mapping**: Create algorithm to link CVEs to vendors via CPE names
6. **Asset-Vendor Linking**: Script to assign vendor_id to existing assets based on naming patterns
7. **Risk Score Calculation**: Implement vendor risk scoring algorithm (CVE count, avg CVSS, incidents)
8. **EOL Status Automation**: Build scheduled job to update eol_status based on current date
9. **Supply Chain Incident Tracking**: Implement incident ingestion and asset flagging
10. **Support Contract Management**: Build contract CRUD operations and expiration alerts
11. **Maintenance Scheduler**: Implement scheduling algorithm prioritizing EOL and criticality
12. **API Development**: Build 10 vendor tracking endpoints
13. **Frontend Dashboard**: Create vendor risk and EOL tracking visualizations
14. **Testing**: Vendor risk scenarios and maintenance scheduling validation
15. **Documentation**: Create vendor tracking guide and API documentation

---

#### 7. Test Requirements

**Unit Tests:**
```javascript
// Test vendor risk score calculation
test('Vendor with 50 CVEs and avg CVSS 8.5 should have high risk score', async () => {
  const vendor = await getVendor('vendor_123');
  expect(vendor.risk_score).toBeGreaterThan(7.0);
});

// Test EOL status automation
test('Asset with EOL date in 90 days should be flagged as approaching_eol', async () => {
  const asset = await getAsset('asset_123');
  expect(asset.eol_status).toBe('approaching_eol');
});

// Test supply chain incident flagging
test('SolarWinds incident should flag all Orion assets', async () => {
  const incident = await createSupplyChainIncident({vendor_id: 'solarwinds', ...});
  const affectedAssets = await getAffectedAssets(incident.incident_id);
  expect(affectedAssets.length).toBeGreaterThan(0);
});

// Test maintenance scheduling
test('Maintenance schedule should prioritize EOL assets', async () => {
  const schedule = await generateMaintenanceSchedule({asset_ids: [...]});
  expect(schedule[0].asset.eol_status).toBe('approaching_eol');
});
```

**Integration Tests:**
- Test endoflife.date API integration with sample products
- Test vendor risk assessment with 10 vendors and 100 CVEs
- Test support contract expiration alerts
- Test maintenance scheduler with 50 assets

**Acceptance Tests:**
- Register 20 vendors with risk scores
- Link 100 assets to vendors and equipment models
- Generate EOL reports for assets expiring in 180 days
- Create maintenance schedule prioritizing critical EOL assets

**Minimum Coverage**: 80% for vendor tracking logic

---

#### 8. Audit Checklist

- [ ] All assets linked to valid Vendor and EquipmentModel nodes
- [ ] Vendor risk scores calculated and updated daily
- [ ] EOL status automation runs daily and flags approaching EOL assets
- [ ] Supply chain incidents tracked and assets flagged within 24 hours
- [ ] Support contract expiration alerts sent 90 days before expiry
- [ ] Maintenance scheduler prioritizes by EOL, criticality, and vulnerability count
- [ ] Documentation covers vendor tracking workflows and API usage

---

#### 9. Rollback Plan

**Pre-Implementation Backup:**
```bash
# Backup Neo4j before vendor schema
neo4j-admin dump --database=neo4j --to=/backup/pre-vendor-tracking.dump

# Export current asset-vendor mappings
MATCH (a:Asset)
RETURN a.asset_id, a.vendor_id, a.model_id
// Export to CSV
```

**Rollback Steps:**
1. Stop vendor tracking ETL pipelines
2. Restore Neo4j from backup dump
3. Remove vendor-specific indexes and constraints
4. Remove endoflife.date API integration
5. Revert API endpoints to previous version
6. Clear vendor dashboard components

**Rollback Time**: < 40 minutes

---

#### 10. Estimated Story Points

**Complexity Factors:**
- Schema design: 3 points
- EOL API integration: 3 points
- Vendor risk scoring: 4 points
- Supply chain incident tracking: 4 points
- Maintenance scheduling: 3 points
- Frontend dashboard: 3 points
- Testing & validation: 5 points

**Total**: 25 story points (High complexity, multiple external integrations)

---

---

## Deferred Phase D1: Safety & Reliability

### E08: RAMS Reliability Analysis

⏸️ **DEFERRED - Phase D1 - Post-MVP**

**Enhancement ID**: E08
**Name**: RAMS (Reliability, Availability, Maintainability, Safety) Analysis
**Deferred Phase**: D1 - Safety & Reliability
**Deferred Reason**: Not frontend-visible, can build on MVP foundation
**Priority**: HIGH
**ICE Score**: 21 (Impact: 8, Confidence: 7, Ease: 6)
**Feasibility**: 0.75
**Estimated Days**: 10 days

---

#### 1. Objective Statement

Integrate RAMS (Reliability, Availability, Maintainability, Safety) engineering principles into the NER11 Gold Model to enable quantitative reliability analysis, failure rate prediction, maintenance optimization, and safety-critical system assessment for industrial and mission-critical assets.

---

#### 2. Acceptance Criteria

**GIVEN** an asset with operational history
**WHEN** reliability analysis is performed
**THEN** the system must calculate MTBF (Mean Time Between Failures), MTTR (Mean Time To Repair), and availability percentage

**GIVEN** a component with known failure modes
**WHEN** RAMS analysis is executed
**THEN** the system must predict failure rates using Weibull distribution and operational stress factors

**GIVEN** a safety-critical system (SIL 3 or higher)
**WHEN** vulnerability impact is assessed
**THEN** the system must calculate probability of failure on demand (PFDavg) and recommend safety integrity level adjustments

**GIVEN** a maintenance schedule for 100 assets
**WHEN** optimizing for cost and availability
**THEN** the system must recommend predictive maintenance intervals minimizing downtime

**GIVEN** a query for assets with availability < 99.5%
**WHEN** filtering by RAMS metrics
**THEN** results must include failure rate trends, maintenance history, and improvement recommendations

**GIVEN** a redundant system configuration
**WHEN** reliability block diagram (RBD) is analyzed
**THEN** the system must calculate series/parallel reliability and identify single points of failure

**GIVEN** performance benchmarks for RAMS calculations
**WHEN** analyzing 1000 assets
**THEN** calculation time must not exceed 5 seconds

---

#### 3. Technical Requirements

**Neo4j Schema Changes:**
```cypher
// RAMS Metrics node
CREATE (rm:RAMSMetrics {
  metrics_id: string,
  asset_id: string,
  measurement_period: string,  // 'daily', 'weekly', 'monthly', 'annual'

  // Reliability metrics
  mtbf: float,  // Mean Time Between Failures (hours)
  failure_rate: float,  // λ (failures per hour)
  reliability_at_time_t: float,  // R(t)

  // Availability metrics
  mttr: float,  // Mean Time To Repair (hours)
  availability: float,  // percentage (0-100)
  uptime_hours: float,
  downtime_hours: float,

  // Maintainability metrics
  mean_maintenance_time: float,
  preventive_maintenance_ratio: float,
  corrective_maintenance_ratio: float,

  // Safety metrics
  sil_level: int,  // Safety Integrity Level (1-4)
  pfd_avg: float,  // Probability of Failure on Demand
  safety_failures: int,
  dangerous_failures: int,

  calculated_at: datetime
});

// Failure Mode node
CREATE (fm:FailureMode {
  failure_mode_id: string,
  asset_id: string,
  mode_name: string,
  failure_mechanism: string,
  detection_method: string,

  // Weibull distribution parameters
  weibull_beta: float,  // shape parameter
  weibull_eta: float,  // scale parameter
  weibull_gamma: float,  // location parameter

  severity: string,  // 'minor', 'moderate', 'major', 'catastrophic'
  occurrence_probability: float,
  detectability: float,
  rpn: int,  // Risk Priority Number (Severity × Occurrence × Detection)

  mitigation_strategy: string,
  last_occurrence: datetime,
  occurrence_count: int
});

// Maintenance Event node
CREATE (me:MaintenanceEvent {
  event_id: string,
  asset_id: string,
  event_type: string,  // 'preventive', 'corrective', 'predictive', 'emergency'
  scheduled_date: datetime,
  actual_date: datetime,
  duration_hours: float,

  work_performed: string,
  parts_replaced: [string],
  technician_id: string,
  cost: float,

  failure_mode_id: string,  // if corrective
  prevented_failure: boolean,
  notes: string
});

// Reliability Block Diagram (RBD) node
CREATE (rbd:ReliabilityBlockDiagram {
  rbd_id: string,
  system_id: string,
  topology: string,  // 'series', 'parallel', 'k-out-of-n', 'complex'
  components: [string],  // list of asset_ids

  system_reliability: float,
  critical_path: [string],
  single_points_of_failure: [string],

  calculated_at: datetime
});

// Add RAMS properties to Asset node
MATCH (a:Asset)
SET a.rams_category = string,  // 'safety_critical', 'mission_critical', 'business_critical', 'non_critical'
    a.redundancy_level = string,  // 'none', 'cold_standby', 'hot_standby', 'n+1', '2n'
    a.sil_target = int,  // Target Safety Integrity Level
    a.operational_stress = float,  // 0.0-1.0 (environmental/load stress)
    a.design_life_hours = float;

// Relationships
CREATE (a:Asset)-[:HAS_RAMS_METRICS]->(rm:RAMSMetrics);
CREATE (a:Asset)-[:HAS_FAILURE_MODE]->(fm:FailureMode);
CREATE (a:Asset)-[:HAS_MAINTENANCE_EVENT]->(me:MaintenanceEvent);
CREATE (a:Asset)-[:PART_OF_RBD]->(rbd:ReliabilityBlockDiagram);
CREATE (fm:FailureMode)-[:MITIGATED_BY]->(me:MaintenanceEvent);
```

**API Endpoints:**

| Method | Path | Payload | Response |
|--------|------|---------|----------|
| POST | `/api/v1/rams/calculate` | `{asset_id, period}` | `{mtbf, mttr, availability, ...}` |
| GET | `/api/v1/rams/metrics/:asset_id` | `?period=monthly` | `{metrics, trends}` |
| POST | `/api/v1/rams/failure-mode` | `{asset_id, mode_name, weibull_params}` | `{failure_mode_id, rpn}` |
| GET | `/api/v1/rams/failure-modes/:asset_id` | - | `[failure_modes]` |
| POST | `/api/v1/rams/predict-failure` | `{asset_id, time_horizon}` | `{probability, predicted_date}` |
| POST | `/api/v1/rams/rbd-analysis` | `{system_id, components}` | `{system_reliability, spof}` |
| GET | `/api/v1/rams/sil-assessment/:asset_id` | - | `{current_sil, target_sil, pfd_avg}` |
| POST | `/api/v1/rams/optimize-maintenance` | `{asset_ids, constraints}` | `{schedule: [...]}` |
| GET | `/api/v1/rams/availability-report` | `?threshold=99.5` | `[assets_below_threshold]` |
| POST | `/api/v1/maintenance/log-event` | `{asset_id, event_type, duration, ...}` | `{event_id}` |

**Frontend Components:**
- RAMSDashboard with MTBF/MTTR/Availability metrics
- WeibullDistributionChart for failure prediction
- ReliabilityBlockDiagramVisualization
- MaintenanceScheduleOptimizer
- SILAssessmentWidget

**Data Integrations:**
- Neo4j: RAMS metrics, failure modes, maintenance events
- CMMS (Computerized Maintenance Management System): Maintenance history
- SCADA/Historians: Operational data for stress calculations
- Asset management system: Equipment inventory

---

#### 4. Dependencies

**Enhancement Dependencies:**
- E01: Customer Labels (Multi-Tenant) - Required for customer-specific RAMS data
- E15: Vendor Equipment Tracking - Provides equipment models and EOL data

**External Dependencies:**
- CMMS systems for maintenance history
- Operational historians (e.g., OSIsoft PI, Wonderware) for failure event data
- Weibull analysis libraries (e.g., Python lifelines, R survival)

**Internal Dependencies:**
- Neo4j graph database
- NER11 Gold Model Asset entities
- Time-series database for operational metrics

---

#### 5. Data Sources

**Internal:**
- Neo4j: Existing Asset nodes requiring RAMS analysis
- Maintenance logs: Historical repair and downtime data
- Failure event logs: System incident tracking

**External:**
- **OREDA (Offshore Reliability Data)**: https://www.oreda.com/
  - Reliability data for offshore equipment
- **IEEE Gold Book (IEEE 493)**: Industrial/commercial power system reliability data
- **IEC 61508 Tables**: Safety integrity level (SIL) requirements
- **NIST SEMATECH Handbook**: Reliability engineering data
- **Vendor reliability specifications**: MTBF/MTTR from equipment datasheets

**Specific Datasets:**
- Maintenance history CSV exports from CMMS
- Failure event logs from SCADA systems
- Vendor MTBF specifications for equipment models

---

#### 6. Implementation Steps

1. **RAMS Framework Research**: Study IEC 61508, OREDA, IEEE 493 for standards
2. **Schema Design**: Define RAMSMetrics, FailureMode, MaintenanceEvent, RBD nodes
3. **Schema Implementation**: Execute Cypher DDL for RAMS entities
4. **MTBF/MTTR Calculation**: Implement algorithms from maintenance event history
5. **Weibull Analysis Integration**: Integrate Python lifelines library for failure prediction
6. **Availability Calculation**: Build formulas for uptime/downtime analysis
7. **SIL Assessment**: Implement PFDavg calculation per IEC 61508
8. **Failure Mode Modeling**: Create RPN calculation and failure mode classification
9. **RBD Analysis**: Implement series/parallel reliability algorithms
10. **Maintenance Optimization**: Build predictive maintenance scheduling algorithm
11. **CMMS Integration**: Build ETL pipeline for maintenance history ingestion
12. **API Development**: Build 10 RAMS analysis endpoints
13. **Frontend Dashboard**: Create RAMS visualization components
14. **Testing**: Validate RAMS calculations with known reliability datasets
15. **Documentation**: Create RAMS analysis guide and API documentation

---

#### 7. Test Requirements

**Unit Tests:**
```javascript
// Test MTBF calculation
test('Asset with 3 failures in 1000 hours should have MTBF ~333 hours', async () => {
  const metrics = await calculateRAMS('asset_123', {period: 'monthly'});
  expect(metrics.mtbf).toBeCloseTo(333, 1);
});

// Test availability calculation
test('Asset with 8760h uptime and 240h downtime should have 97.3% availability', async () => {
  const metrics = await calculateRAMS('asset_456');
  expect(metrics.availability).toBeCloseTo(97.3, 1);
});

// Test Weibull prediction
test('Component with β=2.5, η=10000 should have 30% failure probability at 5000h', async () => {
  const prediction = await predictFailure('component_789', {time_horizon: 5000});
  expect(prediction.probability).toBeCloseTo(0.30, 2);
});

// Test RBD analysis
test('Series system with 3 components (R=0.9 each) should have system R=0.729', async () => {
  const rbd = await analyzeRBD({topology: 'series', components: ['a', 'b', 'c']});
  expect(rbd.system_reliability).toBeCloseTo(0.729, 3);
});

// Test SIL assessment
test('Safety function with PFDavg=1e-4 should be SIL 3', async () => {
  const sil = await assessSIL('safety_function_123');
  expect(sil.sil_level).toBe(3);
});
```

**Integration Tests:**
- Test CMMS integration with 500 maintenance events
- Test Weibull analysis with OREDA reliability data
- Test RBD analysis with complex system (10 components, mixed topology)
- Test maintenance optimization for 50 assets over 1-year horizon

**Acceptance Tests:**
- Calculate RAMS metrics for 100 industrial assets
- Predict failure dates for 20 components using Weibull analysis
- Generate SIL assessment report for safety-critical system
- Optimize maintenance schedule reducing downtime by 15%

**Minimum Coverage**: 80% for RAMS calculation logic

---

#### 8. Audit Checklist

- [ ] MTBF/MTTR calculations validated against IEEE 493 standards
- [ ] Weibull distribution parameters fit historical failure data with R² > 0.85
- [ ] Availability calculations match operational historian data (±1%)
- [ ] SIL assessments align with IEC 61508 PFDavg thresholds
- [ ] RBD analysis identifies all single points of failure
- [ ] Maintenance optimization reduces downtime while staying within budget
- [ ] Documentation covers RAMS methodologies and API usage

---

#### 9. Rollback Plan

**Pre-Implementation Backup:**
```bash
# Backup Neo4j before RAMS schema
neo4j-admin dump --database=neo4j --to=/backup/pre-rams.dump

# Export maintenance history
MATCH (a:Asset)-[:HAS_MAINTENANCE_EVENT]->(me:MaintenanceEvent)
RETURN a.asset_id, me.event_type, me.actual_date, me.duration_hours
// Export to CSV
```

**Rollback Steps:**
1. Stop RAMS calculation scheduled jobs
2. Restore Neo4j from backup dump
3. Remove RAMS-specific indexes and constraints
4. Remove Weibull analysis integration
5. Revert API endpoints to previous version
6. Clear RAMS dashboard components

**Rollback Time**: < 50 minutes

---

#### 10. Estimated Story Points

**Complexity Factors:**
- RAMS framework research: 3 points
- Schema design: 3 points
- MTBF/MTTR/Availability algorithms: 5 points
- Weibull analysis integration: 5 points
- RBD analysis: 4 points
- Maintenance optimization: 5 points
- Frontend visualization: 3 points
- Testing & validation: 5 points

**Total**: 33 story points (Very high complexity, specialized reliability engineering)

---

### E09: Hazard & FMEA Integration

⏸️ **DEFERRED - Phase D1 - Post-MVP**

**Enhancement ID**: E09
**Name**: Hazard Analysis and FMEA (Failure Mode and Effects Analysis)
**Deferred Phase**: D1 - Safety & Reliability
**Deferred Reason**: Depends on E08, not frontend-visible
**Priority**: HIGH
**ICE Score**: 20 (Impact: 8, Confidence: 7, Ease: 5)
**Feasibility**: 0.70
**Estimated Days**: 8 days

---

#### 1. Objective Statement

Integrate systematic hazard analysis and FMEA methodologies into the NER11 Gold Model to enable proactive identification of failure modes, severity assessment, risk prioritization through RPN (Risk Priority Number), and automated hazard tracking for safety-critical systems.

---

#### 2. Acceptance Criteria

**GIVEN** a system component with known failure modes
**WHEN** FMEA analysis is performed
**THEN** the system must calculate RPN (Risk Priority Number) based on Severity × Occurrence × Detection scores

**GIVEN** a hazard identified in a safety-critical system
**WHEN** the hazard is registered
**THEN** it must be classified by severity (1-4: Negligible, Marginal, Critical, Catastrophic) and probability (A-E: Frequent to Improbable)

**GIVEN** a vulnerability linked to a failure mode
**WHEN** the vulnerability is exploited
**THEN** the system must trace cascading hazards through dependent components

**GIVEN** a query for high-risk failure modes
**WHEN** filtering by RPN > 200
**THEN** results must include failure causes, effects, current controls, and recommended actions

**GIVEN** an FMEA worksheet for a subsystem
**WHEN** the worksheet is exported
**THEN** it must conform to SAE J1739 or MIL-STD-1629 standards

**GIVEN** a hazard mitigation implemented
**WHEN** the mitigation is validated
**THEN** the system must recalculate RPN showing risk reduction percentage

**GIVEN** performance benchmarks for FMEA calculations
**WHEN** analyzing 100 failure modes
**THEN** calculation time must not exceed 3 seconds

---

#### 3. Technical Requirements

**Neo4j Schema Changes:**
```cypher
// Hazard node
CREATE (h:Hazard {
  hazard_id: string,
  asset_id: string,
  hazard_name: string,
  description: string,

  // MIL-STD-882E classification
  severity: string,  // '1-Catastrophic', '2-Critical', '3-Marginal', '4-Negligible'
  probability: string,  // 'A-Frequent', 'B-Probable', 'C-Occasional', 'D-Remote', 'E-Improbable'
  risk_matrix_code: string,  // e.g., '1A' (Catastrophic-Frequent) = Unacceptable

  hazard_category: string,  // 'Safety', 'Health', 'Environmental', 'Security'
  initiating_event: string,
  hazardous_condition: string,
  worst_case_effect: string,

  current_controls: [string],
  risk_acceptance_status: string,  // 'acceptable', 'unacceptable', 'acceptable_with_review'

  identified_date: datetime,
  last_review_date: datetime,
  responsible_party: string
});

// FMEA (Failure Mode and Effects Analysis) node
CREATE (fmea:FMEA {
  fmea_id: string,
  asset_id: string,
  component_name: string,
  function: string,

  // Failure mode details
  failure_mode: string,
  failure_cause: string,
  failure_effect_local: string,
  failure_effect_system: string,
  failure_effect_end_user: string,

  // RPN calculation (1-10 scale)
  severity_score: int,  // 1=Minor inconvenience, 10=Catastrophic
  occurrence_score: int,  // 1=Unlikely, 10=Very high
  detection_score: int,  // 1=Almost certain detection, 10=No detection
  rpn: int,  // Severity × Occurrence × Detection (max 1000)

  // Current controls
  current_prevention_controls: [string],
  current_detection_controls: [string],

  // Recommended actions
  recommended_actions: [string],
  action_responsible: string,
  action_target_date: date,
  action_status: string,  // 'open', 'in_progress', 'completed', 'deferred'

  // Post-action RPN
  severity_score_post: int,
  occurrence_score_post: int,
  detection_score_post: int,
  rpn_post: int,
  risk_reduction_percentage: float,

  fmea_standard: string,  // 'SAE J1739', 'MIL-STD-1629', 'IEC 60812'
  created_date: datetime,
  last_updated: datetime
});

// Hazard Mitigation node
CREATE (hm:HazardMitigation {
  mitigation_id: string,
  hazard_id: string,
  mitigation_type: string,  // 'eliminate', 'substitute', 'engineering_control', 'administrative_control', 'ppe'
  description: string,
  implementation_cost: float,
  effectiveness_rating: float,  // 0.0-1.0
  status: string,  // 'proposed', 'approved', 'implemented', 'validated'
  verification_method: string,
  verification_date: date,
  responsible_party: string
});

// Bow-Tie Analysis node (for complex hazard analysis)
CREATE (bt:BowTieAnalysis {
  bowtie_id: string,
  hazard_id: string,
  top_event: string,  // Central hazard event

  // Left side: Threats and preventive barriers
  threats: [string],
  preventive_barriers: [map],  // [{threat, barrier, effectiveness}]

  // Right side: Consequences and mitigative barriers
  consequences: [string],
  mitigative_barriers: [map],  // [{consequence, barrier, effectiveness}]

  escalation_factors: [string],
  residual_risk: string
});

// Add FMEA properties to existing entities
MATCH (a:Asset)
SET a.fmea_completion_status = string,  // 'not_started', 'in_progress', 'completed', 'reviewed'
    a.total_rpn_score = int,  // Sum of all FMEA RPNs for this asset
    a.critical_failure_modes_count = int;

MATCH (v:Vulnerability)
SET v.triggers_hazard = boolean,
    v.hazard_severity = string;

// Relationships
CREATE (a:Asset)-[:HAS_HAZARD]->(h:Hazard);
CREATE (a:Asset)-[:HAS_FMEA]->(fmea:FMEA);
CREATE (h:Hazard)-[:MITIGATED_BY]->(hm:HazardMitigation);
CREATE (h:Hazard)-[:ANALYZED_BY]->(bt:BowTieAnalysis);
CREATE (fmea:FMEA)-[:IDENTIFIED_HAZARD]->(h:Hazard);
CREATE (v:Vulnerability)-[:TRIGGERS]->(h:Hazard);
CREATE (v:Vulnerability)-[:CAUSES_FAILURE_MODE]->(fmea:FMEA);
```

**API Endpoints:**

| Method | Path | Payload | Response |
|--------|------|---------|----------|
| POST | `/api/v1/hazards` | `{asset_id, severity, probability, description}` | `{hazard_id, risk_matrix_code}` |
| GET | `/api/v1/hazards/:id` | - | `{hazard, controls, mitigations}` |
| GET | `/api/v1/hazards/risk-matrix` | - | `{matrix: [...], unacceptable_count}` |
| POST | `/api/v1/fmea` | `{asset_id, failure_mode, severity, occurrence, detection}` | `{fmea_id, rpn}` |
| GET | `/api/v1/fmea/:id` | - | `{fmea, recommended_actions}` |
| GET | `/api/v1/fmea/high-rpn` | `?threshold=200` | `[fmea_entries]` |
| POST | `/api/v1/fmea/:id/action-taken` | `{action_description, rpn_post}` | `{risk_reduction_percentage}` |
| POST | `/api/v1/hazards/:id/mitigation` | `{mitigation_type, description, cost}` | `{mitigation_id}` |
| POST | `/api/v1/hazards/:id/bow-tie` | `{threats, consequences, barriers}` | `{bowtie_id, residual_risk}` |
| GET | `/api/v1/fmea/worksheet/:asset_id` | `?standard=SAE_J1739` | `{worksheet_pdf}` |
| GET | `/api/v1/hazards/cascading-analysis/:hazard_id` | - | `{affected_assets, secondary_hazards}` |

**Frontend Components:**
- RiskMatrixHeatmap (5×5 severity-probability grid)
- FMEAWorksheet component (editable table)
- BowTieVisualization (interactive diagram)
- RPNTrendChart (over time)
- HazardTracker dashboard

**Data Integrations:**
- Neo4j: Hazard, FMEA, Mitigation nodes
- Asset management system: Component hierarchy
- Safety incident database: Historical hazard data
- Vulnerability database: CVE-to-hazard mapping

---

#### 4. Dependencies

**Enhancement Dependencies:**
- E01: Customer Labels (Multi-Tenant) - Required for customer-specific hazard data
- E08: RAMS Reliability Analysis - Provides failure rate data for FMEA occurrence scores

**External Dependencies:**
- Safety standards: MIL-STD-882E, IEC 61508, SAE J1739
- Incident databases: OSHA, HSE, RIDDOR for historical hazard data
- Failure mode libraries: IEEE 1413, IEC 60812

**Internal Dependencies:**
- Neo4j graph database
- NER11 Gold Model Asset and Vulnerability entities
- Safety incident tracking system

---

#### 5. Data Sources

**Internal:**
- Neo4j: Existing Asset and Vulnerability nodes
- Incident logs: Historical safety incidents and near-misses
- RAMS data: Failure rates and maintenance history (from E08)

**External:**
- **OREDA**: Offshore reliability and failure mode data
- **NPRD (Nonelectronic Parts Reliability Data)**: Mechanical component failure modes
- **IEEE 1413-2010**: Failure mode catalog for power systems
- **IEC 60812**: FMEA methodology and examples
- **OSHA Incident Database**: Historical safety hazards
- **NASA FMEA/CIL Database**: Critical items and failure modes

**Specific Datasets:**
- Failure mode templates from IEC 60812 Annex B
- Historical RPN data from automotive FMEA (SAE J1739)
- Bow-tie analysis examples from Energy Institute

---

#### 6. Implementation Steps

1. **Standards Research**: Study MIL-STD-882E, SAE J1739, IEC 60812 for FMEA methodologies
2. **Schema Design**: Define Hazard, FMEA, HazardMitigation, BowTieAnalysis nodes
3. **Schema Implementation**: Execute Cypher DDL for hazard analysis entities
4. **Risk Matrix Implementation**: Build 5×5 severity-probability risk matrix (MIL-STD-882E)
5. **RPN Calculation**: Implement Severity × Occurrence × Detection formula
6. **Failure Mode Library**: Import failure mode templates from IEC 60812
7. **Hazard-Vulnerability Linking**: Create algorithm to link CVEs to hazards
8. **Cascading Hazard Analysis**: Build graph traversal for secondary hazards
9. **Bow-Tie Analysis**: Implement threat-barrier-consequence modeling
10. **Mitigation Tracking**: Build mitigation workflow (propose → approve → implement → validate)
11. **FMEA Worksheet Generator**: Create SAE J1739/MIL-STD-1629 compliant exports
12. **API Development**: Build 11 hazard/FMEA endpoints
13. **Frontend Dashboard**: Create risk matrix, FMEA worksheet, bow-tie visualizations
14. **Testing**: Validate RPN calculations and hazard cascading logic
15. **Documentation**: Create FMEA/hazard analysis guide and API documentation

---

#### 7. Test Requirements

**Unit Tests:**
```javascript
// Test RPN calculation
test('FMEA with Severity=9, Occurrence=7, Detection=5 should have RPN=315', async () => {
  const fmea = await createFMEA({severity: 9, occurrence: 7, detection: 5});
  expect(fmea.rpn).toBe(315);
});

// Test risk matrix classification
test('Hazard with Severity=1 (Catastrophic) and Probability=A (Frequent) should be Unacceptable', async () => {
  const hazard = await createHazard({severity: '1-Catastrophic', probability: 'A-Frequent'});
  expect(hazard.risk_matrix_code).toBe('1A');
  expect(hazard.risk_acceptance_status).toBe('unacceptable');
});

// Test risk reduction calculation
test('RPN reduction from 400 to 100 should show 75% risk reduction', async () => {
  const fmea = await updateFMEA('fmea_123', {rpn_post: 100});
  expect(fmea.risk_reduction_percentage).toBeCloseTo(75, 1);
});

// Test cascading hazard analysis
test('Hazard in Asset A should identify secondary hazards in connected Asset B', async () => {
  const cascade = await analyzeCascadingHazards('hazard_123');
  expect(cascade.secondary_hazards.length).toBeGreaterThan(0);
});
```

**Integration Tests:**
- Test FMEA worksheet generation with 20 failure modes
- Test hazard-vulnerability linking with 50 CVEs
- Test bow-tie analysis with 5 threats and 3 consequences
- Test mitigation workflow from proposal to validation

**Acceptance Tests:**
- Create risk matrix with 30 hazards across all severity-probability combinations
- Conduct FMEA for industrial system with 15 components
- Generate SAE J1739-compliant FMEA worksheet (PDF export)
- Validate risk reduction of 50% after implementing 10 mitigations

**Minimum Coverage**: 80% for FMEA/hazard analysis logic

---

#### 8. Audit Checklist

- [ ] All hazards classified per MIL-STD-882E severity-probability matrix
- [ ] RPN calculations validated against SAE J1739 examples
- [ ] FMEA worksheets conform to industry standards (SAE J1739 or MIL-STD-1629)
- [ ] Hazard-vulnerability links reviewed for accuracy (random sample of 10%)
- [ ] Cascading hazard analysis identifies all secondary effects
- [ ] Mitigation effectiveness ratings validated by subject matter experts
- [ ] Documentation covers FMEA methodologies and hazard workflows

---

#### 9. Rollback Plan

**Pre-Implementation Backup:**
```bash
# Backup Neo4j before hazard schema
neo4j-admin dump --database=neo4j --to=/backup/pre-fmea-hazard.dump

# Export existing FMEA data (if any)
MATCH (a:Asset)-[:HAS_FMEA]->(fmea:FMEA)
RETURN a.asset_id, fmea.failure_mode, fmea.rpn
// Export to CSV
```

**Rollback Steps:**
1. Stop hazard analysis scheduled jobs
2. Restore Neo4j from backup dump
3. Remove FMEA/Hazard-specific indexes and constraints
4. Remove hazard-vulnerability linkage algorithms
5. Revert API endpoints to previous version
6. Clear hazard tracking dashboard components

**Rollback Time**: < 45 minutes

---

#### 10. Estimated Story Points

**Complexity Factors:**
- Standards research: 3 points
- Schema design: 4 points
- RPN and risk matrix: 4 points
- Failure mode library: 3 points
- Cascading hazard analysis: 5 points
- Bow-tie analysis: 4 points
- FMEA worksheet generation: 3 points
- Frontend visualizations: 4 points
- Testing & validation: 5 points

**Total**: 35 story points (Very high complexity, safety engineering expertise required)

---

---

## MVP Phase B2: Supply Chain (continued)

### E03: SBOM Vulnerability Analysis

🟡 **MVP ENHANCEMENT - Phase B2 - Order 4**

**Enhancement ID**: E03
**Name**: SBOM (Software Bill of Materials) Vulnerability Analysis
**MVP Phase**: B2 - Supply Chain
**MVP Order**: 4 of 6
**Priority**: HIGH
**ICE Score**: 8.0
**Estimated Days**: 12 days (Days 33-44 of MVP)

---

#### 1. Objective Statement

Integrate comprehensive SBOM (Software Bill of Materials) analysis into the NER11 Gold Model to enable automated software component vulnerability tracking, license compliance verification, supply chain risk assessment, and dependency chain analysis for modern software assets.

---

#### 2. Acceptance Criteria

**GIVEN** an SBOM file in CycloneDX or SPDX format
**WHEN** the SBOM is imported
**THEN** all software components must be parsed, deduplicated, and linked to CVE databases

**GIVEN** a software component with known vulnerabilities
**WHEN** the component is analyzed
**THEN** the system must return all applicable CVEs with CVSS scores and exploitability metrics

**GIVEN** a dependency chain with transitive vulnerabilities
**WHEN** risk assessment is performed
**THEN** the system must trace vulnerabilities through all dependency levels

**GIVEN** a query for open-source components with license restrictions
**WHEN** filtering by license type
**THEN** results must include GPL, AGPL, and other copyleft licenses with compliance warnings

**GIVEN** a software asset with 500 components
**WHEN** SBOM analysis is executed
**THEN** processing time must not exceed 30 seconds

**GIVEN** a new CVE published for a tracked component
**WHEN** the CVE is ingested
**THEN** all assets using that component must be automatically flagged within 1 hour

**GIVEN** an SBOM export request
**WHEN** generating CycloneDX JSON
**THEN** the export must conform to CycloneDX 1.5 specification

---

#### 3. Technical Requirements

**Neo4j Schema Changes:**
```cypher
// Software Component node
CREATE (sc:SoftwareComponent {
  component_id: string,
  name: string,
  version: string,
  purl: string,  // Package URL (e.g., pkg:npm/lodash@4.17.21)
  cpe: string,   // Common Platform Enumeration

  component_type: string,  // 'library', 'framework', 'application', 'operating-system', 'device', 'firmware'
  supplier: string,
  author: string,
  publisher: string,

  // License information
  license: string,
  license_type: string,  // 'permissive', 'copyleft', 'proprietary', 'public_domain'
  license_risk: string,  // 'low', 'medium', 'high'

  // Package metadata
  ecosystem: string,  // 'npm', 'maven', 'pypi', 'cargo', 'nuget', 'apt'
  repository_url: string,
  homepage_url: string,
  download_url: string,

  // Vulnerability summary
  known_vulnerabilities_count: int,
  highest_cvss_score: float,
  exploitable_vulnerabilities_count: int,

  // Supply chain metadata
  malicious_package_flag: boolean,
  typosquatting_flag: boolean,
  abandoned_package_flag: boolean,
  last_update_date: date,

  // Hashes for verification
  sha256: string,
  sha512: string,

  created_at: datetime,
  last_scanned: datetime
});

// SBOM (Software Bill of Materials) node
CREATE (sbom:SBOM {
  sbom_id: string,
  asset_id: string,
  sbom_format: string,  // 'CycloneDX', 'SPDX'
  sbom_version: string,  // '1.5', '2.3'

  serial_number: string,
  timestamp: datetime,

  // Summary statistics
  total_components: int,
  vulnerable_components_count: int,
  critical_vulnerabilities_count: int,
  high_risk_licenses_count: int,

  // Compliance
  compliance_status: string,  // 'compliant', 'non_compliant', 'review_required'
  compliance_frameworks: [string],  // ['NTIA_SBOM', 'EO14028']

  metadata: map
});

// Dependency relationship
CREATE (sc1:SoftwareComponent)-[:DEPENDS_ON {
  dependency_type: string,  // 'direct', 'indirect', 'dev', 'optional'
  scope: string,  // 'runtime', 'test', 'provided'
  version_constraint: string  // '>=4.17.0 <5.0.0'
}]->(sc2:SoftwareComponent);

// Software Vulnerability (links CVE to components)
CREATE (sv:SoftwareVulnerability {
  vulnerability_id: string,
  cve_id: string,
  component_id: string,

  affected_versions: [string],
  fixed_version: string,
  patch_available: boolean,

  // CVSS scores
  cvss_v3_score: float,
  cvss_v3_vector: string,
  cvss_v2_score: float,

  // Exploitability
  exploit_available: boolean,
  exploit_maturity: string,  // 'unproven', 'poc', 'functional', 'high'
  epss_score: float,  // Exploit Prediction Scoring System

  // Impact
  confidentiality_impact: string,
  integrity_impact: string,
  availability_impact: string,

  // Remediation
  remediation_type: string,  // 'update', 'patch', 'workaround', 'none'
  workaround_available: boolean,
  workaround_description: string,

  published_date: datetime,
  last_modified_date: datetime
});

// Add SBOM properties to Asset
MATCH (a:Asset)
SET a.has_sbom = boolean,
    a.sbom_last_updated = datetime,
    a.software_component_count = int,
    a.vulnerable_component_count = int;

// Relationships
CREATE (a:Asset)-[:HAS_SBOM]->(sbom:SBOM);
CREATE (sbom:SBOM)-[:CONTAINS]->(sc:SoftwareComponent);
CREATE (sc:SoftwareComponent)-[:HAS_VULNERABILITY]->(sv:SoftwareVulnerability);
CREATE (sv:SoftwareVulnerability)-[:REFERENCES]->(cve:CVE);
CREATE (a:Asset)-[:USES_COMPONENT]->(sc:SoftwareComponent);
```

**API Endpoints:**

| Method | Path | Payload | Response |
|--------|------|---------|----------|
| POST | `/api/v1/sbom/import` | `{format, file_content}` | `{sbom_id, components_count}` |
| GET | `/api/v1/sbom/:id` | - | `{sbom, components, vulnerabilities}` |
| GET | `/api/v1/sbom/:id/export` | `?format=cyclonedx` | `{sbom_json}` |
| GET | `/api/v1/sbom/:id/vulnerabilities` | `?severity=critical` | `[vulnerabilities]` |
| GET | `/api/v1/sbom/:id/dependency-graph` | - | `{graph_data}` |
| GET | `/api/v1/components/:id/vulnerabilities` | - | `[vulnerabilities]` |
| POST | `/api/v1/components/search` | `{name, version}` | `[matching_components]` |
| GET | `/api/v1/components/:id/affected-assets` | - | `[assets]` |
| GET | `/api/v1/sbom/:id/license-compliance` | - | `{high_risk_licenses, compliance_status}` |
| POST | `/api/v1/sbom/diff` | `{sbom_id_1, sbom_id_2}` | `{added, removed, updated}` |
| GET | `/api/v1/sbom/supply-chain-risk/:component_id` | - | `{risk_factors, malicious_flags}` |

**Frontend Components:**
- SBOMViewer with component tree
- DependencyGraphVisualization (interactive graph)
- VulnerabilityTimeline
- LicenseComplianceMatrix
- SupplyChainRiskDashboard

**Data Integrations:**
- Neo4j: SBOM, SoftwareComponent, SoftwareVulnerability nodes
- NVD CVE API: Vulnerability data
- OSV (Open Source Vulnerabilities): Multi-ecosystem vulnerability database
- GitHub Advisory Database: Security advisories
- Snyk, Sonatype OSS Index: Additional vulnerability data

---

#### 4. Dependencies

**Enhancement Dependencies:**
- E01: Customer Labels (Multi-Tenant) - Required for customer-specific SBOMs

**External Dependencies:**
- CycloneDX specification: https://cyclonedx.org/
- SPDX specification: https://spdx.dev/
- NVD CVE API: https://nvd.nist.gov/developers
- OSV API: https://osv.dev/
- Package ecosystem APIs (npm, PyPI, Maven Central)

**Internal Dependencies:**
- Neo4j graph database
- NER11 Gold Model CVE entities
- Asset management system

---

#### 5. Data Sources

**Internal:**
- Neo4j: Existing CVE and Asset nodes
- NER11 Gold Model: 189,932 entities for vulnerability linking

**External:**
- **NVD CVE API**: https://services.nvd.nist.gov/rest/json/cves/2.0
  - ~25,000 CVEs per year
- **OSV (Open Source Vulnerabilities)**: https://osv.dev/
  - Multi-ecosystem vulnerability database (npm, PyPI, Go, etc.)
- **GitHub Advisory Database**: https://github.com/advisories
  - ~20,000 security advisories
- **EPSS (Exploit Prediction Scoring System)**: https://www.first.org/epss/
  - Daily exploit likelihood scores
- **Snyk Vulnerability DB**: https://snyk.io/vuln/
  - Additional vulnerability intelligence
- **ClearlyDefined**: https://clearlydefined.io/
  - License and component metadata

**Specific Datasets:**
- CycloneDX example SBOMs for testing
- SPDX 2.3 example documents
- License compatibility matrix from SPDX

---

#### 6. Implementation Steps

1. **SBOM Standards Research**: Study CycloneDX 1.5 and SPDX 2.3 specifications
2. **Schema Design**: Define SBOM, SoftwareComponent, SoftwareVulnerability nodes
3. **Schema Implementation**: Execute Cypher DDL for SBOM entities
4. **SBOM Parser**: Build CycloneDX/SPDX parser with schema validation
5. **Component Deduplication**: Implement fuzzy matching for duplicate components (purl-based)
6. **NVD Integration**: Build ETL pipeline for CVE-to-component mapping
7. **OSV Integration**: Build ETL pipeline for ecosystem-specific vulnerabilities
8. **Dependency Graph Construction**: Implement dependency chain resolution
9. **License Risk Assessment**: Build license classification logic (permissive/copyleft/proprietary)
10. **Supply Chain Risk Scoring**: Implement malicious package detection (typosquatting, abandonment)
11. **SBOM Export**: Build CycloneDX 1.5 and SPDX 2.3 export functionality
12. **API Development**: Build 11 SBOM analysis endpoints
13. **Frontend Dashboard**: Create SBOM viewer, dependency graph, vulnerability timeline
14. **Testing**: Validate SBOM parsing with 10 real-world examples (npm, Maven, PyPI)
15. **Documentation**: Create SBOM analysis guide and API documentation

---

#### 7. Test Requirements

**Unit Tests:**
```javascript
// Test SBOM parsing
test('CycloneDX 1.5 SBOM with 100 components should parse successfully', async () => {
  const sbom = await importSBOM({format: 'cyclonedx', file_content: cyclonedxJson});
  expect(sbom.total_components).toBe(100);
});

// Test component deduplication
test('Duplicate components should be merged by purl', async () => {
  const sbom = await importSBOM({...});
  const components = await getComponents(sbom.sbom_id);
  const purls = components.map(c => c.purl);
  expect(new Set(purls).size).toBe(purls.length); // No duplicates
});

// Test vulnerability matching
test('lodash@4.17.15 should match CVE-2020-8203', async () => {
  const component = await getComponent({name: 'lodash', version: '4.17.15'});
  const vulns = await getVulnerabilities(component.component_id);
  expect(vulns.some(v => v.cve_id === 'CVE-2020-8203')).toBe(true);
});

// Test license risk classification
test('Component with GPL-3.0 license should be flagged as high risk', async () => {
  const component = await createComponent({license: 'GPL-3.0'});
  expect(component.license_risk).toBe('high');
});

// Test dependency chain resolution
test('Express should show transitive dependencies including accepts', async () => {
  const deps = await getDependencyChain('express@4.18.0');
  expect(deps.some(d => d.name === 'accepts')).toBe(true);
});
```

**Integration Tests:**
- Test SBOM import pipeline with 500-component CycloneDX file
- Test NVD CVE matching for 100 npm components
- Test OSV API integration for PyPI vulnerabilities
- Test SBOM export conformance to CycloneDX 1.5 schema

**Acceptance Tests:**
- Import 5 real-world SBOMs (npm, Maven, PyPI, Go, Rust)
- Identify 50 vulnerabilities across imported components
- Generate license compliance report showing 10 high-risk licenses
- Export SBOM in both CycloneDX and SPDX formats

**Minimum Coverage**: 80% for SBOM parsing and vulnerability matching logic

---

#### 8. Audit Checklist

- [ ] SBOM parsing conforms to CycloneDX 1.5 and SPDX 2.3 specifications
- [ ] Component deduplication eliminates 100% of purl-based duplicates
- [ ] Vulnerability matching achieves >95% accuracy (validated against Snyk/Dependabot)
- [ ] License risk classification aligns with SPDX license list
- [ ] Dependency chain resolution handles transitive dependencies correctly
- [ ] SBOM exports pass CycloneDX/SPDX schema validation
- [ ] Documentation covers SBOM workflows and API usage

---

#### 9. Rollback Plan

**Pre-Implementation Backup:**
```bash
# Backup Neo4j before SBOM schema
neo4j-admin dump --database=neo4j --to=/backup/pre-sbom.dump

# Backup existing component data (if any)
MATCH (sc:SoftwareComponent)
RETURN sc.name, sc.version, sc.purl
// Export to CSV
```

**Rollback Steps:**
1. Stop SBOM import/export services
2. Restore Neo4j from backup dump
3. Remove SBOM-specific indexes and constraints
4. Remove NVD/OSV integration pipelines
5. Revert API endpoints to previous version
6. Clear SBOM dashboard components

**Rollback Time**: < 35 minutes

---

#### 10. Estimated Story Points

**Complexity Factors:**
- SBOM standards research: 2 points
- Schema design: 3 points
- CycloneDX/SPDX parser: 5 points
- Component deduplication: 3 points
- NVD/OSV integration: 4 points
- Dependency graph: 4 points
- License risk assessment: 2 points
- Frontend visualization: 3 points
- Testing & validation: 5 points

**Total**: 31 story points (High complexity, multiple external integrations)

---

---

## MVP Phase B3: Prioritization

### E10: Economic Impact Modeling

🟡 **MVP ENHANCEMENT - Phase B3 - Order 5**

**Enhancement ID**: E10
**Name**: Economic Impact Analysis
**MVP Phase**: B3 - Prioritization
**MVP Order**: 5 of 6
**Priority**: HIGH
**ICE Score**: 7.8
**Estimated Days**: 10 days (Days 45-54 of MVP)

---

#### 1. Objective Statement

Integrate economic impact modeling into the NER11 Gold Model to enable breach cost calculation, ROI analysis, and sector-specific investment prioritization for cybersecurity decisions.

---

#### 2. Acceptance Criteria

**GIVEN** a vulnerability affecting a specific sector
**WHEN** economic impact is calculated
**THEN** the system must return breach cost estimates based on IBM Breach Report data

**GIVEN** a remediation investment scenario
**WHEN** ROI analysis is performed
**THEN** the system must calculate expected return based on risk reduction

**GIVEN** a sector-specific query
**WHEN** filtering by industry
**THEN** results must include sector-adjusted cost multipliers

---

#### 3. Technical Requirements

**Data Sources:**
- IBM Breach Report 2025 ($4.44M avg)
- FRED API
- World Bank indicators
- Kaggle breach datasets

**Frontend Components:**
- Economic impact dashboard
- ROI calculator widget
- Sector comparison charts

---

### E12: NOW/NEXT/NEVER Prioritization

🔴 **MVP ENHANCEMENT - Phase B3 - Order 6**

**Enhancement ID**: E12
**Name**: NOW/NEXT/NEVER CVE Prioritization
**MVP Phase**: B3 - Prioritization
**MVP Order**: 6 of 6
**Priority**: CRITICAL
**ICE Score**: 8.5
**Estimated Days**: 8 days (Days 55-62 of MVP)

---

#### 1. Objective Statement

Implement NOW/NEXT/NEVER prioritization framework to reduce 316K CVEs to actionable priorities, achieving 99.8% noise reduction while ensuring critical vulnerabilities are addressed immediately.

---

#### 2. Acceptance Criteria

**GIVEN** 316K CVEs in the database
**WHEN** NOW/NEXT/NEVER scoring is applied
**THEN** ~0.2% should be NOW, ~0.8% NEXT, ~99% NEVER

**GIVEN** a CVE marked as NOW
**WHEN** organizational context is applied
**THEN** the CVE must have active exploitation AND relevance to organizational assets

**GIVEN** sector-specific thresholds
**WHEN** prioritization is calculated
**THEN** results must reflect sector-adjusted risk tolerance

---

#### 3. Technical Requirements

**Key Deliverables:**
1. NOW/NEXT/NEVER scoring algorithm
2. `PriorityAssessment` node type
3. 5.06M assessment nodes (316K × 16 sectors)
4. Cognitive bias integration
5. Sector-specific thresholds
6. Resource allocation optimization

**Frontend Components:**
- NOW/NEXT/NEVER CVE table
- Priority badges (NOW=red, NEXT=yellow, NEVER=gray)
- Sector-specific views
- Action queue

**Data Sources:**
- NVD CVSS
- EPSS scores
- Organizational profiles

---

## Deferred Phase D2: Advanced Analysis

### E11: Psychohistory Demographics

⏸️ **DEFERRED - Phase D2 - Post-MVP**

**Enhancement ID**: E11
**Name**: Psychohistory Demographics
**Deferred Phase**: D2 - Advanced Analysis
**Deferred Reason**: Complex implementation, not MVP-critical
**Estimated Days**: 8 days

---

### E13: Attack Path Modeling

⏸️ **DEFERRED - Phase D2 - Post-MVP**

**Enhancement ID**: E13
**Name**: Attack Path Modeling
**Deferred Phase**: D2 - Advanced Analysis
**Deferred Reason**: Can build on MVP foundation
**Estimated Days**: 15 days

---

## Deferred Phase D3: Psychometric Core

### E19: Organizational Blind Spots

⏸️ **DEFERRED - Phase D3 - Post-MVP**

**Enhancement ID**: E19
**Name**: Organizational Blind Spots Detection
**Deferred Phase**: D3 - Psychometric Core
**Estimated Days**: 12 days

---

### E20: Personality-Team Fit Analysis

⏸️ **DEFERRED - Phase D3 - Post-MVP**

**Enhancement ID**: E20
**Name**: Personality-Team Fit Analysis
**Deferred Phase**: D3 - Psychometric Core
**Estimated Days**: 12 days

---

### E21: Transcript Psychometric NER

⏸️ **DEFERRED - Phase D3 - Post-MVP**

**Enhancement ID**: E21
**Name**: Transcript Psychometric NER
**Deferred Phase**: D3 - Psychometric Core
**Deferred Reason**: Requires NER11 Gold Model
**Estimated Days**: 15 days

---

### E24: Cognitive Dissonance Detection

⏸️ **DEFERRED - Phase D3 - Post-MVP**

**Enhancement ID**: E24
**Name**: Cognitive Dissonance Breaking
**Deferred Phase**: D3 - Psychometric Core
**Estimated Days**: 10 days

---

### E25: Threat Actor Personality Profiling

⏸️ **DEFERRED - Phase D3 - Post-MVP**

**Enhancement ID**: E25
**Name**: Threat Actor Personality Modeling
**Deferred Phase**: D3 - Psychometric Core
**Deferred Reason**: Requires E13, E21
**Estimated Days**: 12 days

---

## Deferred Phase D4: Experimental Psychohistory

### E17: Lacanian Dyad Analysis

🧪 **EXPERIMENTAL - Phase D4 - Post-MVP**

**Enhancement ID**: E17
**Name**: Lacanian Dyad Analysis
**Deferred Phase**: D4 - Experimental Psychohistory
**Status**: EXPERIMENTAL - Requires extensive validation
**Estimated Days**: 10 days

---

### E18: Triad Group Dynamics

🧪 **EXPERIMENTAL - Phase D4 - Post-MVP**

**Enhancement ID**: E18
**Name**: Triad Group Dynamics
**Deferred Phase**: D4 - Experimental Psychohistory
**Status**: EXPERIMENTAL - Requires extensive validation
**Estimated Days**: 12 days

---

### E22: Seldon Crisis Prediction

🧪 **EXPERIMENTAL - Phase D4 - Post-MVP**

**Enhancement ID**: E22
**Name**: Seldon Crisis Prediction
**Deferred Phase**: D4 - Experimental Psychohistory
**Status**: EXPERIMENTAL - Requires extensive validation
**Estimated Days**: 20 days

---

### E23: Population Event Forecasting

🧪 **EXPERIMENTAL - Phase D4 - Post-MVP**

**Enhancement ID**: E23
**Name**: Population Event Forecasting
**Deferred Phase**: D4 - Experimental Psychohistory
**Status**: EXPERIMENTAL - Requires extensive validation
**Estimated Days**: 18 days

---

## Summary Tables

### MVP Enhancements (6 total, 62 days)

| Order | ID | Name | Phase | Days | Priority |
|-------|-----|------|-------|------|----------|
| 1 | CUSTOMER_LABELS | Multi-Tenant Isolation | B1 | 5 | CRITICAL |
| 2 | E07 | IEC 62443 Industrial Safety | B1 | 15 | CRITICAL |
| 3 | E15 | Vendor Equipment Tracking | B2 | 12 | HIGH |
| 4 | E03 | SBOM Dependency Analysis | B2 | 12 | HIGH |
| 5 | E10 | Economic Impact Analysis | B3 | 10 | HIGH |
| 6 | E12 | NOW/NEXT/NEVER Prioritization | B3 | 8 | CRITICAL |

### Deferred Enhancements (13 total, 162 days)

| Phase | ID | Name | Days | Status |
|-------|-----|------|------|--------|
| D1 | E08 | RAMS Reliability | 10 | DEFERRED |
| D1 | E09 | Hazard & FMEA | 8 | DEFERRED |
| D2 | E11 | Demographics | 8 | DEFERRED |
| D2 | E13 | Attack Path | 15 | DEFERRED |
| D3 | E19 | Blind Spots | 12 | DEFERRED |
| D3 | E20 | Team Fit | 12 | DEFERRED |
| D3 | E21 | Transcript NER | 15 | DEFERRED |
| D3 | E24 | Cognitive Dissonance | 10 | DEFERRED |
| D3 | E25 | Threat Actor | 12 | DEFERRED |
| D4 | E17 | Lacanian Dyad | 10 | EXPERIMENTAL |
| D4 | E18 | Triad Dynamics | 12 | EXPERIMENTAL |
| D4 | E22 | Seldon Crisis | 20 | EXPERIMENTAL |
| D4 | E23 | Population Forecast | 18 | EXPERIMENTAL |

---

## Links

- [00_TASKMASTER_MASTER_INDEX.md](00_TASKMASTER_MASTER_INDEX.md) - Master navigation
- [01_IMPLEMENTATION_ORDER.json](01_IMPLEMENTATION_ORDER.json) - Full enhancement details
- [02_PHASE_DETAILS.md](02_PHASE_DETAILS.md) - Phase breakdown
- [04_PM_CHECKLIST.md](04_PM_CHECKLIST.md) - PM tracking
- [05_SESSION_HANDOFF.md](05_SESSION_HANDOFF.md) - Multi-session handoff
- [../blotter/BLOTTER.md](../blotter/BLOTTER.md) - Activity log

---

**Task Specifications v1.0.1 | Option B: Balanced Foundation MVP | Updated 2025-12-04**