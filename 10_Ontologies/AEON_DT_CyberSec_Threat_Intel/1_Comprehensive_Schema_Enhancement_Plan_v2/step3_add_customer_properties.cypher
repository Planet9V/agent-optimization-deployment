// ===================================================================
// STEP 3: Add Customer Properties to Asset Nodes
// CRITICAL SAFETY: Only use SET, NEVER delete or modify existing data
// Check customer_id IS NULL before setting to avoid overwrites
// ===================================================================

// 3.1 Add Customer Properties to Server Nodes (Customer 1: Energy)
// Assign servers in datacenter DC-PRIMARY-01 to Regional Power Authority
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
RETURN 'Servers assigned to Customer 1 (Energy):' AS description, count(s) AS count;

// 3.2 Add Customer Properties to NetworkDevice Nodes (Customer 2: Water)
// Assign network devices in datacenter DC-SECONDARY-02 to Metropolitan Water District
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
RETURN 'NetworkDevices assigned to Customer 2 (Water):' AS description, count(nd) AS count;

// 3.3 Add Customer Properties to ICS_Asset Nodes (Customer 3: Manufacturing)
// Assign ICS assets in Detroit location to Advanced Manufacturing Corp
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
RETURN 'ICS_Assets assigned to Customer 3 (Manufacturing):' AS description, count(ics) AS count;

// 3.4 Add Customer Properties to saref:Device Nodes (Customer 1: Energy)
// Assign saref:Device nodes in San Francisco to Regional Power Authority
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

// Log updated count
MATCH (d:saref_Device)
WHERE d.customer_id = 'CUST-001-ENERGY'
RETURN 'saref_Devices assigned to Customer 1 (Energy):' AS description, count(d) AS count;

// 3.5 Mark Shared/Multi-Tenant Assets
// Identify and mark shared infrastructure (e.g., shared database servers)
MATCH (s:Server)
WHERE s.server_role CONTAINS 'Shared'
   OR s.hostname CONTAINS 'shared'
   OR s.server_type = 'multi_tenant'
SET s.shared_asset = true,
    s.ownership_status = 'multi_tenant',
    s.tenant_list = ['CUST-001-ENERGY', 'CUST-002-WATER'],
    s.primary_tenant = 'CUST-001-ENERGY';

// Log shared asset count
MATCH (s:Server)
WHERE s.shared_asset = true
RETURN 'Servers marked as shared/multi-tenant:' AS description, count(s) AS count;

// 3.6 Create Index on customer_id for Fast Filtering
// Create range index for customer_id across all node types
CREATE INDEX asset_customer_id_idx IF NOT EXISTS
FOR (n)
ON (n.customer_id);

// Create index on organization_id
CREATE INDEX asset_organization_id_idx IF NOT EXISTS
FOR (n)
ON (n.organization_id);

RETURN 'Indexes created successfully' AS status;

// 3.7 Validation Query
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

// CRITICAL CVE CHECK - Verify no CVE nodes were accidentally modified
MATCH (cve:CVE)
WHERE EXISTS(cve.customer_id)
RETURN count(cve) AS incorrectly_modified_cves;
// EXPECTED: 0 (ABORT if > 0)
