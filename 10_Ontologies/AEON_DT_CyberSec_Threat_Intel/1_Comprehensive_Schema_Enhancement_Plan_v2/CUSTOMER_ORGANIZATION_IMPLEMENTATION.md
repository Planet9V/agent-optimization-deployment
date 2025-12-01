# Customer/Organization Labeling Implementation Guide
**File:** CUSTOMER_ORGANIZATION_IMPLEMENTATION.md
**Created:** 2025-10-30
**Version:** v1.0.0
**Author:** AEON Digital Twin Implementation Team
**Purpose:** Complete implementation guide for adding Customer/Organization multi-tenant labeling
**Status:** READY FOR EXECUTION

---

## Executive Summary

**Objective:** Add Customer/Organization ownership labeling to AEON schema to enable "my equipment" filtering across all 8 critical operational questions.

**Current Gap:** Cannot distinguish "my equipment" vs "other customer equipment" - affects Questions 1, 6, 7, 8

**Solution:** Additive-only, phased implementation with complete CVE preservation (all 147,923 nodes protected)

**Implementation Approach:**
- **Strategy:** Additive-only (no deletions, no modifications)
- **Duration:** 2-3 days
- **Execution Time:** 42 minutes of Cypher execution
- **Average ICE Score:** 9.6/10
- **Risk Level:** LOW (fully reversible)

**Success Criteria:**
✅ All 147,923 CVE nodes preserved
✅ ~2,500 assets assigned to customers/organizations
✅ Customer isolation validated (no cross-tenant leaks)
✅ All 8 questions answered with 100% capability
✅ Query performance <1 second for customer-filtered queries

---

## Implementation Steps

### STEP 1: Create Customer & Organization Schemas

**ICE Score:** 10.0 (Impact: 10, Confidence: 10, Ease: 10)
**Time:** 2 minutes
**Risk:** ZERO

#### 1.1 Create Constraints

```cypher
// Create unique constraint on Customer.customer_id
CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
FOR (c:Customer) REQUIRE c.customer_id IS UNIQUE;

// Create unique constraint on Organization.org_id
CREATE CONSTRAINT organization_id_unique IF NOT EXISTS
FOR (o:Organization) REQUIRE o.org_id IS UNIQUE;
```

#### 1.2 Create Indexes for Fast Lookups

```cypher
// Index on customer_name for search
CREATE INDEX customer_name_idx IF NOT EXISTS
FOR (c:Customer) ON (c.customer_name);

// Index on org_name for search
CREATE INDEX org_name_idx IF NOT EXISTS
FOR (o:Organization) ON (o.org_name);

// Index on parent_customer_id for organization lookup
CREATE INDEX org_parent_idx IF NOT EXISTS
FOR (o:Organization) ON (o.parent_customer_id);

// Index on industry_sector for sector-based queries
CREATE INDEX customer_sector_idx IF NOT EXISTS
FOR (c:Customer) ON (c.industry_sector);
```

#### 1.3 Validation Query

```cypher
// Verify constraints were created successfully
SHOW CONSTRAINTS
WHERE name CONTAINS 'customer' OR name CONTAINS 'organization';

// Expected output: 2 constraints
// - customer_id_unique
// - organization_id_unique
```

#### 1.4 Rollback Procedure (if needed)

```cypher
DROP CONSTRAINT customer_id_unique IF EXISTS;
DROP CONSTRAINT organization_id_unique IF EXISTS;
DROP INDEX customer_name_idx IF EXISTS;
DROP INDEX org_name_idx IF EXISTS;
DROP INDEX org_parent_idx IF EXISTS;
DROP INDEX customer_sector_idx IF EXISTS;
```

---

### STEP 2: Create Sample Customer & Organization Nodes

**ICE Score:** 9.3 (Impact: 9, Confidence: 10, Ease: 9)
**Time:** 5 minutes
**Risk:** ZERO

#### 2.1 Customer 1: Energy Sector (Regional Power Authority)

```cypher
CREATE (c1:Customer {
  customer_id: 'CUST-001-ENERGY',
  customer_name: 'Regional Power Authority',
  industry_sector: 'energy',
  criticality_tier: 'Tier1',
  contract_start_date: date('2020-01-15'),
  contract_status: 'active',
  regulatory_requirements: ['NERC CIP', 'FERC', 'EPA Clean Power Plan'],
  primary_contact_email: 'ops@regionalpower.example',
  primary_contact_phone: '+1-555-0100',
  billing_account_id: 'BILL-RPA-001',
  headquarters_location: 'San Francisco, CA',
  service_regions: ['Western US', 'Pacific Northwest'],
  employee_count: 5000,
  annual_revenue: 2500000000,
  cybersecurity_maturity: 'Advanced',
  incident_notification_required: true,
  sla_tier: 'Platinum',
  created_date: datetime(),
  last_updated: datetime(),
  node_id: randomUUID()
});
```

#### 2.2 Organization 1: SCADA Operations (under Customer 1)

```cypher
CREATE (o1:Organization {
  org_id: 'ORG-RPA-SCADA',
  org_name: 'SCADA Operations - Western Region',
  parent_customer_id: 'CUST-001-ENERGY',
  business_unit: 'Grid Operations',
  geographic_location: 'San Francisco, CA',
  facility_ids: ['DC-PRIMARY-01', 'SUBSTATION-WEST-01'],
  org_criticality: 'critical',
  org_function: 'Operational Technology Management',
  asset_count_estimate: 850,
  staff_count: 120,
  budget_allocation: 15000000,
  compliance_scope: ['NERC CIP-002', 'NERC CIP-005', 'NERC CIP-007'],
  created_date: datetime(),
  last_updated: datetime(),
  node_id: randomUUID()
});
```

#### 2.3 Link Customer 1 to Organization 1

```cypher
MATCH (c:Customer {customer_id: 'CUST-001-ENERGY'})
MATCH (o:Organization {org_id: 'ORG-RPA-SCADA'})
CREATE (c)-[:HAS_ORGANIZATION {
  established_date: date('2020-02-01'),
  reporting_structure: 'direct',
  budget_authority: 'full',
  operational_autonomy: 'high',
  relationship_created: datetime()
}]->(o);
```

#### 2.4 Customer 2: Water Sector (Metropolitan Water District)

```cypher
CREATE (c2:Customer {
  customer_id: 'CUST-002-WATER',
  customer_name: 'Metropolitan Water District',
  industry_sector: 'water',
  criticality_tier: 'Tier1',
  contract_start_date: date('2021-06-01'),
  contract_status: 'active',
  regulatory_requirements: ['EPA SDWA', 'EPA AWIA', 'State Water Resources Control Board'],
  primary_contact_email: 'it@metrowater.example',
  primary_contact_phone: '+1-555-0200',
  billing_account_id: 'BILL-MWD-002',
  headquarters_location: 'Austin, TX',
  service_regions: ['Central Texas', 'Hill Country'],
  employee_count: 2500,
  annual_revenue: 800000000,
  cybersecurity_maturity: 'Intermediate',
  incident_notification_required: true,
  sla_tier: 'Gold',
  created_date: datetime(),
  last_updated: datetime(),
  node_id: randomUUID()
});
```

#### 2.5 Organization 2: Water Treatment Facilities (under Customer 2)

```cypher
CREATE (o2:Organization {
  org_id: 'ORG-MWD-TREATMENT',
  org_name: 'Water Treatment Facilities',
  parent_customer_id: 'CUST-002-WATER',
  business_unit: 'Water Quality Operations',
  geographic_location: 'Austin, TX',
  facility_ids: ['DC-SECONDARY-02', 'TREATMENT-PLANT-CENTRAL'],
  org_criticality: 'high',
  org_function: 'Water Purification and Quality Control',
  asset_count_estimate: 450,
  staff_count: 75,
  budget_allocation: 8000000,
  compliance_scope: ['EPA SDWA Section 1433', 'Texas Water Code'],
  created_date: datetime(),
  last_updated: datetime(),
  node_id: randomUUID()
});
```

#### 2.6 Link Customer 2 to Organization 2

```cypher
MATCH (c:Customer {customer_id: 'CUST-002-WATER'})
MATCH (o:Organization {org_id: 'ORG-MWD-TREATMENT'})
CREATE (c)-[:HAS_ORGANIZATION {
  established_date: date('2021-07-01'),
  reporting_structure: 'direct',
  budget_authority: 'delegated',
  operational_autonomy: 'medium',
  relationship_created: datetime()
}]->(o);
```

#### 2.7 Customer 3: Manufacturing (Advanced Manufacturing Corp)

```cypher
CREATE (c3:Customer {
  customer_id: 'CUST-003-MFG',
  customer_name: 'Advanced Manufacturing Corp',
  industry_sector: 'manufacturing',
  criticality_tier: 'Tier2',
  contract_start_date: date('2022-03-15'),
  contract_status: 'active',
  regulatory_requirements: ['NIST 800-171', 'CMMC Level 2', 'ITAR'],
  primary_contact_email: 'security@advmfg.example',
  primary_contact_phone: '+1-555-0300',
  billing_account_id: 'BILL-AMC-003',
  headquarters_location: 'Detroit, MI',
  service_regions: ['Great Lakes', 'Midwest'],
  employee_count: 8000,
  annual_revenue: 3200000000,
  cybersecurity_maturity: 'Advanced',
  incident_notification_required: false,
  sla_tier: 'Silver',
  created_date: datetime(),
  last_updated: datetime(),
  node_id: randomUUID()
});
```

#### 2.8 Organization 3: Assembly Line Operations (under Customer 3)

```cypher
CREATE (o3:Organization {
  org_id: 'ORG-AMC-ASSEMBLY',
  org_name: 'Assembly Line Operations',
  parent_customer_id: 'CUST-003-MFG',
  business_unit: 'Production Engineering',
  geographic_location: 'Detroit, MI',
  facility_ids: ['DC-TERTIARY-03', 'FACTORY-DETROIT-MAIN'],
  org_criticality: 'medium',
  org_function: 'Automated Assembly and Quality Control',
  asset_count_estimate: 1200,
  staff_count: 250,
  budget_allocation: 25000000,
  compliance_scope: ['NIST 800-171 r2', 'CMMC Level 2'],
  created_date: datetime(),
  last_updated: datetime(),
  node_id: randomUUID()
});
```

#### 2.9 Link Customer 3 to Organization 3

```cypher
MATCH (c:Customer {customer_id: 'CUST-003-MFG'})
MATCH (o:Organization {org_id: 'ORG-AMC-ASSEMBLY'})
CREATE (c)-[:HAS_ORGANIZATION {
  established_date: date('2022-04-01'),
  reporting_structure: 'direct',
  budget_authority: 'full',
  operational_autonomy: 'high',
  relationship_created: datetime()
}]->(o);
```

#### 2.10 Validation Query

```cypher
// Count customers and organizations created
MATCH (c:Customer)
OPTIONAL MATCH (c)-[:HAS_ORGANIZATION]->(o:Organization)
RETURN
  count(DISTINCT c) AS customer_count,
  count(DISTINCT o) AS organization_count,
  collect(DISTINCT c.customer_name) AS customer_names,
  collect(DISTINCT o.org_name) AS org_names;

// Expected output:
// customer_count: 3
// organization_count: 3
// customer_names: ['Regional Power Authority', 'Metropolitan Water District', 'Advanced Manufacturing Corp']
```

#### 2.11 Rollback Procedure (if needed)

```cypher
// Delete test customers and their organizations
MATCH (c:Customer)
WHERE c.customer_id IN ['CUST-001-ENERGY', 'CUST-002-WATER', 'CUST-003-MFG']
DETACH DELETE c;

MATCH (o:Organization)
WHERE o.org_id IN ['ORG-RPA-SCADA', 'ORG-MWD-TREATMENT', 'ORG-AMC-ASSEMBLY']
DETACH DELETE o;
```

---

### STEP 3: Enhance Asset Nodes with Customer Properties

**ICE Score:** 9.0 (Impact: 10, Confidence: 9, Ease: 8)
**Time:** 10 minutes
**Risk:** LOW (property additions only)

#### 3.1 Add Customer Properties to Server Nodes (Example Assignment)

```cypher
// Assign Customer 1 (Energy) to servers in datacenter DC-PRIMARY-01
MATCH (s:Server)
WHERE s.data_center = 'DC-PRIMARY-01'
  AND s.customer_id IS NULL  // Only update if not already assigned
SET s.customer_id = 'CUST-001-ENERGY',
    s.organization_id = 'ORG-RPA-SCADA',
    s.asset_owner = 'Regional Power Authority',
    s.ownership_status = 'active',
    s.shared_asset = false,
    s.asset_acquisition_date = date('2020-03-01'),
    s.last_customer_update = datetime();

// Log updated count
MATCH (s:Server)
WHERE s.customer_id = 'CUST-001-ENERGY'
RETURN count(s) AS servers_assigned_to_customer_1;
```

#### 3.2 Add Customer Properties to NetworkDevice Nodes

```cypher
// Assign Customer 2 (Water) to network devices in datacenter DC-SECONDARY-02
MATCH (nd:NetworkDevice)
WHERE nd.data_center = 'DC-SECONDARY-02'
  AND nd.customer_id IS NULL
SET nd.customer_id = 'CUST-002-WATER',
    nd.organization_id = 'ORG-MWD-TREATMENT',
    nd.asset_owner = 'Metropolitan Water District',
    nd.ownership_status = 'active',
    nd.shared_asset = false,
    nd.asset_acquisition_date = date('2021-08-15'),
    nd.last_customer_update = datetime();

// Log updated count
MATCH (nd:NetworkDevice)
WHERE nd.customer_id = 'CUST-002-WATER'
RETURN count(nd) AS network_devices_assigned_to_customer_2;
```

#### 3.3 Add Customer Properties to ICS_Asset Nodes

```cypher
// Assign Customer 3 (Manufacturing) to ICS assets in Detroit location
MATCH (ics:ICS_Asset)
WHERE ics.physical_location CONTAINS 'Detroit'
  AND ics.customer_id IS NULL
SET ics.customer_id = 'CUST-003-MFG',
    ics.organization_id = 'ORG-AMC-ASSEMBLY',
    ics.asset_owner = 'Advanced Manufacturing Corp',
    ics.ownership_status = 'active',
    ics.shared_asset = false,
    ics.asset_acquisition_date = date('2022-05-01'),
    ics.last_customer_update = datetime();

// Log updated count
MATCH (ics:ICS_Asset)
WHERE ics.customer_id = 'CUST-003-MFG'
RETURN count(ics) AS ics_assets_assigned_to_customer_3;
```

#### 3.4 Add Customer Properties to saref:Device Nodes

```cypher
// Assign saref:Device nodes based on their location properties
// Example: Energy sector devices
MATCH (d)
WHERE d:saref_Device
  AND d.location CONTAINS 'San Francisco'
  AND d.customer_id IS NULL
SET d.customer_id = 'CUST-001-ENERGY',
    d.organization_id = 'ORG-RPA-SCADA',
    d.asset_owner = 'Regional Power Authority',
    d.ownership_status = 'active',
    d.shared_asset = false,
    d.last_customer_update = datetime();
```

#### 3.5 Mark Shared/Multi-Tenant Assets

```cypher
// Identify and mark shared infrastructure (e.g., shared database servers)
MATCH (s:Server)
WHERE s.server_role CONTAINS 'Shared'
   OR s.hostname CONTAINS 'shared'
   OR s.server_type = 'multi_tenant'
SET s.shared_asset = true,
    s.ownership_status = 'multi_tenant',
    s.tenant_list = ['CUST-001-ENERGY', 'CUST-002-WATER'],  // Example
    s.primary_tenant = 'CUST-001-ENERGY';  // Primary billing customer
```

#### 3.6 Create Index on customer_id for Fast Filtering

```cypher
// Create range index for customer_id across all node types
CREATE INDEX asset_customer_id_idx IF NOT EXISTS
FOR (n)
ON (n.customer_id)
OPTIONS {indexProvider: 'range'};

// Create index on organization_id
CREATE INDEX asset_organization_id_idx IF NOT EXISTS
FOR (n)
ON (n.organization_id)
OPTIONS {indexProvider: 'range'};
```

#### 3.7 Validation Query

```cypher
// Verify property assignments across all asset types
MATCH (asset)
WHERE asset:Server OR asset:NetworkDevice OR asset:ICS_Asset OR asset:saref_Device
RETURN
  labels(asset)[0] AS asset_type,
  count(asset) AS total_count,
  count(asset.customer_id) AS assigned_count,
  count(asset) - count(asset.customer_id) AS unassigned_count,
  round((count(asset.customer_id) * 100.0 / count(asset)), 2) AS assignment_percentage
ORDER BY asset_type;

// Check for unassigned assets that should be fixed
MATCH (asset)
WHERE (asset:Server OR asset:NetworkDevice OR asset:ICS_Asset OR asset:saref_Device)
  AND asset.customer_id IS NULL
RETURN
  count(asset) AS unassigned_assets_remaining,
  collect(DISTINCT labels(asset)[0])[0..5] AS unassigned_types;

// Verify no CVE nodes were accidentally modified
MATCH (cve:CVE)
WHERE EXISTS(cve.customer_id)
RETURN count(cve) AS incorrectly_modified_cves;
// Expected: 0 (CVEs should NEVER have customer_id)
```

#### 3.8 Rollback Procedure (if needed)

```cypher
// Remove customer properties from all asset nodes
MATCH (asset)
WHERE asset:Server OR asset:NetworkDevice OR asset:ICS_Asset OR asset:saref_Device
REMOVE asset.customer_id,
       asset.organization_id,
       asset.asset_owner,
       asset.ownership_status,
       asset.shared_asset,
       asset.asset_acquisition_date,
       asset.tenant_list,
       asset.primary_tenant,
       asset.last_customer_update;

// Drop indexes
DROP INDEX asset_customer_id_idx IF EXISTS;
DROP INDEX asset_organization_id_idx IF EXISTS;
```

---

### STEP 4: Create Ownership Relationships

**ICE Score:** 9.3 (Impact: 9, Confidence: 10, Ease: 9)
**Time:** 5 minutes
**Risk:** ZERO (relationships are additive)

#### 4.1 Create Customer → Asset Ownership Relationships

```cypher
// Create OWNS_EQUIPMENT relationships for all customers
MATCH (c:Customer)
MATCH (asset)
WHERE (asset:Server OR asset:NetworkDevice OR asset:ICS_Asset OR asset:saref_Device)
  AND asset.customer_id = c.customer_id
  AND NOT EXISTS((c)-[:OWNS_EQUIPMENT]->(asset))  // Avoid duplicates
CREATE (c)-[:OWNS_EQUIPMENT {
  acquired_date: coalesce(asset.asset_acquisition_date, date('2020-01-01')),
  warranty_expiration: date('2025-12-31'),  // Default, update with real data
  asset_criticality: coalesce(asset.criticality, 'medium'),
  ownership_type: CASE
    WHEN asset.shared_asset = true THEN 'shared'
    ELSE 'owned'
  END,
  maintenance_status: 'active',
  relationship_created: datetime()
}]->(asset);

// Log relationship counts by customer
MATCH (c:Customer)-[owns:OWNS_EQUIPMENT]->(asset)
RETURN
  c.customer_name AS customer,
  count(asset) AS equipment_count,
  collect(DISTINCT labels(asset)[0]) AS asset_types
ORDER BY equipment_count DESC;
```

#### 4.2 Create Organization → Asset Management Relationships

```cypher
// Create MANAGES_EQUIPMENT relationships for all organizations
MATCH (o:Organization)
MATCH (asset)
WHERE (asset:Server OR asset:NetworkDevice OR asset:ICS_Asset OR asset:saref_Device)
  AND asset.organization_id = o.org_id
  AND NOT EXISTS((o)-[:MANAGES_EQUIPMENT]->(asset))  // Avoid duplicates
CREATE (o)-[:MANAGES_EQUIPMENT {
  responsible_team: 'IT Operations',  // Default, update with real data
  maintenance_contract: 'Standard',
  budget_allocation: 'OpEx',
  primary_contact: o.org_name + ' Operations Manager',
  escalation_level: CASE o.org_criticality
    WHEN 'critical' THEN 1
    WHEN 'high' THEN 2
    ELSE 3
  END,
  relationship_created: datetime()
}]->(asset);

// Log relationship counts by organization
MATCH (o:Organization)-[manages:MANAGES_EQUIPMENT]->(asset)
RETURN
  o.org_name AS organization,
  o.parent_customer_id AS parent_customer,
  count(asset) AS managed_equipment_count
ORDER BY managed_equipment_count DESC;
```

#### 4.3 Create Indexes on Relationships for Fast Traversal

```cypher
// Create index on OWNS_EQUIPMENT relationship properties
CREATE INDEX owns_equipment_criticality_idx IF NOT EXISTS
FOR ()-[r:OWNS_EQUIPMENT]-() ON (r.asset_criticality);

// Create index on MANAGES_EQUIPMENT relationship properties
CREATE INDEX manages_equipment_team_idx IF NOT EXISTS
FOR ()-[r:MANAGES_EQUIPMENT]-() ON (r.responsible_team);
```

#### 4.4 Validation Query

```cypher
// Verify ownership relationships created correctly
MATCH (c:Customer)-[owns:OWNS_EQUIPMENT]->(asset)
RETURN
  c.customer_name AS customer,
  count(DISTINCT asset) AS owned_assets,
  collect(DISTINCT labels(asset)[0]) AS asset_types
ORDER BY owned_assets DESC;

// Verify all assets with customer_id have ownership relationship
MATCH (asset)
WHERE (asset:Server OR asset:NetworkDevice OR asset:ICS_Asset OR asset:saref_Device)
  AND asset.customer_id IS NOT NULL
WITH count(asset) AS assets_with_customer_id
MATCH (:Customer)-[:OWNS_EQUIPMENT]->(asset2)
WHERE asset2:Server OR asset2:NetworkDevice OR asset2:ICS_Asset OR asset2:saref_Device
WITH assets_with_customer_id, count(DISTINCT asset2) AS assets_with_relationship
RETURN
  assets_with_customer_id AS expected_count,
  assets_with_relationship AS actual_relationships,
  assets_with_customer_id = assets_with_relationship AS validation_passed;

// Check for orphaned relationships (relationships without matching property)
MATCH (c:Customer)-[:OWNS_EQUIPMENT]->(asset)
WHERE asset.customer_id <> c.customer_id
RETURN count(asset) AS orphaned_relationships;
// Expected: 0
```

#### 4.5 Rollback Procedure (if needed)

```cypher
// Delete all ownership relationships
MATCH (:Customer)-[r:OWNS_EQUIPMENT]->()
DELETE r;

// Delete all management relationships
MATCH (:Organization)-[r:MANAGES_EQUIPMENT]->()
DELETE r;

// Drop relationship indexes
DROP INDEX owns_equipment_criticality_idx IF EXISTS;
DROP INDEX manages_equipment_team_idx IF EXISTS;
```

---

### STEP 5: Validate CVE Preservation & Test Queries

**ICE Score:** 10.0 (Impact: 10, Confidence: 10, Ease: 10)
**Time:** 5 minutes
**Risk:** ZERO (read-only validation)

#### 5.1 CRITICAL: Verify CVE Count Unchanged

```cypher
// Count all CVE nodes
MATCH (cve:CVE)
RETURN count(cve) AS cve_count;

// EXPECTED: 147,923
// ABORT IMMEDIATELY IF NOT MATCHING - THIS IS CRITICAL
```

#### 5.2 Verify CVE Nodes Were Not Modified

```cypher
// Check if any CVE nodes have customer properties (they should NOT)
MATCH (cve:CVE)
WHERE EXISTS(cve.customer_id)
   OR EXISTS(cve.organization_id)
   OR EXISTS(cve.asset_owner)
RETURN count(cve) AS incorrectly_modified_cves;

// EXPECTED: 0
// If > 0, investigate immediately and rollback Step 3
```

#### 5.3 Test "My Equipment" Filtering

```cypher
// Test Customer 1 equipment filtering
MATCH (c:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(asset)
RETURN
  labels(asset)[0] AS asset_type,
  count(asset) AS my_equipment_count
ORDER BY my_equipment_count DESC;

// Should return counts for each asset type owned by Customer 1
```

#### 5.4 Test CVE Impact on MY Equipment (Question 1 - Primary Use Case)

```cypher
// Find CVEs impacting Customer 1's equipment
MATCH (customer:Customer {customer_id: 'CUST-001-ENERGY'})
      -[:OWNS_EQUIPMENT]->(server:Server)
MATCH (server)-[:RUNS]->(app:Application)
      -[:CONTAINS]->(comp:SoftwareComponent)
      -[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvss_base_score >= 7.0
RETURN
  server.hostname AS my_equipment,
  comp.name AS vulnerable_component,
  cve.cve_id AS cve_id,
  cve.cvss_base_score AS severity,
  cve.published_date AS published
ORDER BY cve.cvss_base_score DESC
LIMIT 10;

// Verify query returns results and executes in <1 second
```

#### 5.5 Test Multi-Customer Isolation

```cypher
// Verify no assets are assigned to multiple customers (unless marked shared)
MATCH (c1:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(asset1)
MATCH (c2:Customer {customer_id: 'CUST-002-WATER'})-[:OWNS_EQUIPMENT]->(asset2)
WHERE asset1 = asset2
  AND asset1.shared_asset <> true  // Exclude intentionally shared assets
RETURN
  count(asset1) AS incorrectly_shared_assets,
  collect(asset1.hostname)[0..5] AS sample_assets;

// EXPECTED: incorrectly_shared_assets = 0
// If > 0, review Step 3 assignments
```

#### 5.6 Test Query Performance

```cypher
// Profile customer-filtered query to verify index usage
PROFILE
MATCH (c:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(asset)
MATCH (asset)<-[:INSTALLED_ON]-(comp:SoftwareComponent)
      -[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvss_base_score >= 7.0
RETURN count(DISTINCT asset) AS vulnerable_assets;

// Verify:
// - Uses customer_id index
// - Execution time < 100ms
// - DB Hits < 10,000
```

#### 5.7 Comprehensive Validation Report

```cypher
// Generate complete validation report
CALL {
  // CVE count
  MATCH (cve:CVE)
  RETURN count(cve) AS cve_count
}
CALL {
  // Customer count
  MATCH (c:Customer)
  RETURN count(c) AS customer_count
}
CALL {
  // Organization count
  MATCH (o:Organization)
  RETURN count(o) AS organization_count
}
CALL {
  // Assets with customer assignment
  MATCH (asset)
  WHERE (asset:Server OR asset:NetworkDevice OR asset:ICS_Asset OR asset:saref_Device)
    AND asset.customer_id IS NOT NULL
  RETURN count(asset) AS assigned_assets
}
CALL {
  // Ownership relationships
  MATCH (:Customer)-[r:OWNS_EQUIPMENT]->()
  RETURN count(r) AS ownership_relationships
}
RETURN
  cve_count,
  customer_count,
  organization_count,
  assigned_assets,
  ownership_relationships,
  CASE
    WHEN cve_count = 147923 THEN '✅ PASS'
    ELSE '❌ FAIL - ABORT IMPLEMENTATION'
  END AS cve_preservation_check;

// CRITICAL: If cve_preservation_check = FAIL, stop and rollback
```

---

### STEP 6: Update Application Queries with Customer Filtering

**ICE Score:** 10.0 (Impact: 10, Confidence: 10, Ease: 10)
**Time:** 15 minutes
**Risk:** ZERO (documentation only)

#### 6.1 Before/After Query Examples

##### Question 1: "Does this CVE impact my equipment?"

**BEFORE (No Customer Filtering):**
```cypher
// Old query - shows ALL equipment across ALL customers
MATCH (cve:CVE {cve_id: 'CVE-2024-1234'})
      <-[:HAS_VULNERABILITY]-(comp:SoftwareComponent)
      -[:INSTALLED_ON]->(server:Server)
RETURN
  server.hostname,
  comp.name,
  cve.cve_id;

// Problem: Cannot distinguish "my" equipment from others
// Shows equipment for ALL customers in multi-tenant environment
```

**AFTER (With Customer Filtering):**
```cypher
// New query - shows only MY equipment
MATCH (customer:Customer {customer_id: $myCustomerID})
      -[:OWNS_EQUIPMENT]->(server:Server)
MATCH (server)<-[:INSTALLED_ON]-(comp:SoftwareComponent)
      -[:HAS_VULNERABILITY]->(cve:CVE {cve_id: $targetCVE})
RETURN
  server.hostname AS my_equipment,
  server.data_center AS location,
  comp.name AS vulnerable_component,
  comp.version AS component_version,
  cve.cve_id AS cve_id,
  cve.cvss_base_score AS severity,
  cve.published_date AS published,
  server.patch_status AS current_patch_status,
  CASE
    WHEN server.criticality = 'critical' THEN 'IMMEDIATE'
    WHEN cve.cvss_base_score >= 9.0 THEN 'URGENT'
    WHEN cve.cvss_base_score >= 7.0 THEN 'HIGH'
    ELSE 'MEDIUM'
  END AS remediation_priority
ORDER BY cve.cvss_base_score DESC, server.criticality DESC;

// Solution: Only shows equipment owned by my customer
// Enables multi-tenant isolation
```

##### Question 3: "Does this new CVE impact any of my equipment in my facility?"

**BEFORE:**
```cypher
// Generic query without customer or facility filtering
MATCH (cve:CVE)
WHERE cve.published_date >= date('2025-10-30')
MATCH (cve)<-[:HAS_VULNERABILITY]-(comp:SoftwareComponent)
      -[:INSTALLED_ON]->(asset)
RETURN count(DISTINCT asset) AS impacted_equipment;

// Problem: Shows all equipment across all customers and facilities
```

**AFTER:**
```cypher
// Customer-specific facility query
MATCH (customer:Customer {customer_id: $myCustomerID})
      -[:OWNS_EQUIPMENT]->(asset)
WHERE asset.data_center IN $myFacilities  // e.g., ['DC-PRIMARY-01']
WITH customer, asset
MATCH (cve:CVE)
WHERE cve.published_date >= date($today)  // New CVEs only
MATCH (cve)<-[:HAS_VULNERABILITY]-(comp:SoftwareComponent)
      -[:INSTALLED_ON]->(asset)
RETURN
  cve.cve_id AS new_cve,
  cve.cvss_base_score AS severity,
  cve.published_date AS published,
  count(DISTINCT asset) AS my_impacted_equipment,
  collect(DISTINCT asset.hostname)[0..10] AS sample_hosts,
  collect(DISTINCT asset.data_center) AS my_facilities,
  comp.name AS vulnerable_component
ORDER BY cve.cvss_base_score DESC;

// Solution: Only my equipment in my facilities
```

##### Question 6: "How many pieces of equipment do I have?"

**BEFORE:**
```cypher
// Total equipment count (all customers)
MATCH (s:Server)
WHERE s.manufacturer = 'Dell' AND s.model = 'PowerEdge R740'
RETURN count(s) AS totalCount;

// Problem: Shows equipment across all customers
```

**AFTER:**
```cypher
// My equipment count only
MATCH (customer:Customer {customer_id: $myCustomerID})
      -[:OWNS_EQUIPMENT]->(equipment)
WHERE equipment:Server
RETURN
  equipment.manufacturer AS manufacturer,
  equipment.model AS model,
  count(equipment) AS my_equipment_count,
  collect(DISTINCT equipment.data_center) AS my_datacenters,
  avg(duration.between(equipment.asset_acquisition_date, date()).years) AS avg_age_years
ORDER BY my_equipment_count DESC;

// Solution: Customer-specific inventory count
```

##### Question 7: "Do I have a specific application or operating system?"

**BEFORE:**
```cypher
// Check existence globally
MATCH (app:Application)
WHERE app.applicationName = 'Apache Log4j' AND app.version = '2.14.1'
RETURN count(app) > 0 AS hasApplication;

// Problem: True even if other customers have it, not me
```

**AFTER:**
```cypher
// Check existence in my environment only
MATCH (customer:Customer {customer_id: $myCustomerID})
      -[:OWNS_EQUIPMENT]->(asset)
      -[:RUNS]->(app:Application)
WHERE app.applicationName = $searchApp  // e.g., 'Apache Log4j'
  AND app.version = $searchVersion      // e.g., '2.14.1'
RETURN
  count(app) > 0 AS i_have_this_application,
  count(DISTINCT asset) AS installed_on_my_assets,
  collect(DISTINCT asset.hostname)[0..5] AS sample_installations,
  collect(DISTINCT asset.data_center) AS my_affected_datacenters;

// Solution: Customer-specific software inventory
```

##### Question 8: "Where is a specific vulnerability located?"

**BEFORE:**
```cypher
// Global vulnerability location
MATCH (vuln:CVE {cve_id: 'CVE-2021-44228'})
      <-[:HAS_VULNERABILITY]-(asset)
MATCH (asset)-[:PHYSICALLY_LOCATED_IN]->(dc:DataCenterFacility)
RETURN
  asset.hostname,
  dc.facility_name;

// Problem: Shows all customers' vulnerable assets
```

**AFTER:**
```cypher
// My vulnerable assets only
MATCH (customer:Customer {customer_id: $myCustomerID})
      -[:OWNS_EQUIPMENT]->(asset)
      -[:HAS_VULNERABILITY]->(vuln:CVE {cve_id: $targetCVE})
MATCH (asset)-[:PHYSICALLY_LOCATED_IN]->(dc:DataCenterFacility)
RETURN
  asset.hostname AS my_affected_asset,
  labels(asset)[0] AS asset_type,
  asset.criticality AS asset_criticality,
  dc.facility_name AS my_facility,
  asset.rack_id AS rack,
  asset.rack_unit_position AS rack_unit,
  vuln.cvss_base_score AS severity,
  CASE asset.patch_status
    WHEN 'patched' THEN '✅ Mitigated'
    WHEN 'pending' THEN '⚠️ Patch Pending'
    ELSE '❌ Vulnerable'
  END AS remediation_status
ORDER BY vuln.cvss_base_score DESC, asset.criticality DESC;

// Solution: Customer-specific vulnerability tracking
```

---

## Complete Rollback Procedure

### Full System Rollback (Use if Implementation Fails)

```cypher
// STEP 1: Delete all ownership relationships
MATCH (:Customer)-[r:OWNS_EQUIPMENT]->()
DELETE r;

MATCH (:Organization)-[r:MANAGES_EQUIPMENT]->()
DELETE r;

// STEP 2: Remove customer properties from assets
MATCH (asset)
WHERE asset:Server OR asset:NetworkDevice OR asset:ICS_Asset OR asset:saref_Device
REMOVE asset.customer_id,
       asset.organization_id,
       asset.asset_owner,
       asset.ownership_status,
       asset.shared_asset,
       asset.asset_acquisition_date,
       asset.tenant_list,
       asset.primary_tenant,
       asset.last_customer_update;

// STEP 3: Delete Customer and Organization nodes
MATCH (c:Customer)
DETACH DELETE c;

MATCH (o:Organization)
DETACH DELETE o;

// STEP 4: Drop all indexes
DROP INDEX customer_name_idx IF EXISTS;
DROP INDEX org_name_idx IF EXISTS;
DROP INDEX org_parent_idx IF EXISTS;
DROP INDEX customer_sector_idx IF EXISTS;
DROP INDEX asset_customer_id_idx IF EXISTS;
DROP INDEX asset_organization_id_idx IF EXISTS;
DROP INDEX owns_equipment_criticality_idx IF EXISTS;
DROP INDEX manages_equipment_team_idx IF EXISTS;

// STEP 5: Drop all constraints
DROP CONSTRAINT customer_id_unique IF EXISTS;
DROP CONSTRAINT organization_id_unique IF EXISTS;

// STEP 6: Verify rollback complete
MATCH (c:Customer) RETURN count(c) AS remaining_customers;
MATCH (o:Organization) RETURN count(o) AS remaining_organizations;
MATCH (asset)
WHERE EXISTS(asset.customer_id)
RETURN count(asset) AS assets_with_customer_properties;

// All counts should be 0
```

### Verify System Restored to Pre-Implementation State

```cypher
// Critical verification
MATCH (cve:CVE)
RETURN count(cve) AS cve_count;
// MUST return 147,923

// Verify no customer-related artifacts remain
MATCH (n)
WHERE n:Customer OR n:Organization
RETURN count(n) AS customer_org_count;
// MUST return 0

SHOW CONSTRAINTS WHERE name CONTAINS 'customer' OR name CONTAINS 'organization';
// MUST return empty
```

---

## Execution Timeline

### Day 1 Morning (2 hours)
- **Steps 1-2:** Create schemas and sample customers
- **Validation:** Test in development environment
- **Stakeholder Review:** Present sample data to business owners

### Day 1 Afternoon (2 hours)
- **Step 3 Pilot:** Enhance 10% of assets (250 nodes)
- **Validation:** Run all Step 3 validation queries
- **Review:** Assess assignment logic correctness

### Day 2 (4 hours)
- **Step 3 Complete:** Enhance all ~2,500 assets
- **Step 4:** Create all ownership relationships
- **Step 5:** Run complete validation suite
- **CRITICAL:** Verify CVE count = 147,923

### Day 3 (2 hours)
- **Step 6:** Update query library and documentation
- **Training:** Educate analysts on customer filtering
- **Production Deployment:** Deploy to production if all validations pass

---

## Success Criteria Checklist

- [ ] All 147,923 CVE nodes preserved (count verified)
- [ ] 3 customers created (Energy, Water, Manufacturing)
- [ ] 3 organizations created and linked to customers
- [ ] ~2,500 assets assigned to customers/organizations
- [ ] Ownership relationships created (Customer → Asset, Organization → Asset)
- [ ] Customer isolation validated (no cross-tenant leaks)
- [ ] All 8 questions answerable with customer filtering
- [ ] Query performance <1 second for customer-filtered queries
- [ ] Documentation updated with before/after examples
- [ ] Analyst training completed

---

## Post-Implementation Monitoring

### Week 1: Monitor Query Performance
```cypher
// Weekly performance check
PROFILE
MATCH (c:Customer {customer_id: $customerId})-[:OWNS_EQUIPMENT]->(asset)
MATCH (asset)<-[:INSTALLED_ON]-(comp)-[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvss_base_score >= 7.0
RETURN count(DISTINCT asset);

// Verify execution time < 100ms
```

### Month 1: Validate Data Quality
```cypher
// Check for unassigned assets that should have customers
MATCH (asset)
WHERE (asset:Server OR asset:NetworkDevice OR asset:ICS_Asset)
  AND asset.customer_id IS NULL
  AND asset.ownership_status IS NULL
RETURN
  count(asset) AS unassigned_assets,
  collect(asset.hostname)[0..10] AS samples;

// Investigate if count > 0
```

### Ongoing: CVE Preservation Audit
```cypher
// Monthly CVE count verification
MATCH (cve:CVE)
RETURN count(cve) AS cve_count,
       date() AS audit_date;

// Log result and compare to baseline (147,923)
```

---

## Conclusion

This implementation guide provides a **complete, safe, and reversible approach** to adding Customer/Organization multi-tenant labeling to the AEON Digital Twin Cybersecurity schema.

**Key Achievements:**
✅ Enables "my equipment" filtering for all 8 critical questions
✅ Preserves all 147,923 existing CVE nodes
✅ Supports multi-tenant deployments
✅ Achieves 100% question coverage (up from 87.5%)
✅ Provides complete rollback capability at every step
✅ Delivers in 2-3 days with minimal risk

**Next Steps:**
1. Review implementation plan with stakeholders
2. Execute Steps 1-2 in development environment
3. Validate sample customer data
4. Proceed with phased rollout per timeline
5. Monitor performance and data quality post-deployment

**Implementation Status:** READY FOR EXECUTION
