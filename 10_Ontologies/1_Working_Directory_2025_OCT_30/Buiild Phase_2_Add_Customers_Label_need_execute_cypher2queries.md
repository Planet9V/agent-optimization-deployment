 Step 1: Schema Creation (2 minutes)

  Open Neo4j Browser and execute these commands:

  // Create constraints
  CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
  FOR (c:Customer) REQUIRE c.customer_id IS UNIQUE;

  CREATE CONSTRAINT organization_id_unique IF NOT EXISTS
  FOR (o:Organization) REQUIRE o.org_id IS UNIQUE;

  // Create indexes
  CREATE INDEX customer_name_idx IF NOT EXISTS
  FOR (c:Customer) ON (c.customer_name);

  CREATE INDEX org_name_idx IF NOT EXISTS
  FOR (o:Organization) ON (o.org_name);

  CREATE INDEX org_parent_idx IF NOT EXISTS
  FOR (o:Organization) ON (o.parent_customer_id);

  CREATE INDEX customer_sector_idx IF NOT EXISTS
  FOR (c:Customer) ON (c.industry_sector);

  CREATE INDEX asset_customer_id_idx IF NOT EXISTS
  FOR (n) ON (n.customer_id);

  CREATE INDEX asset_organization_id_idx IF NOT EXISTS
  FOR (n) ON (n.organization_id);

  Verify Step 1:
  SHOW CONSTRAINTS WHERE name CONTAINS 'customer' OR name CONTAINS 'organization';
  Expected: 2 constraints listed

  Step 2: Create Customers & Organizations (5 minutes)

  // Customer 1: Energy Sector
  CREATE (c1:Customer {
    customer_id: 'CUST-001-ENERGY',
    customer_name: 'Regional Power Authority',
    industry_sector: 'energy',
    criticality_tier: 'Tier1',
    contract_start_date: date('2020-01-15'),
    contract_status: 'active',
    regulatory_requirements: ['NERC CIP', 'FERC', 'EPA Clean Power Plan'],
    primary_contact_email: 'ops@regionalpower.example',
    created_date: datetime(),
    last_updated: datetime(),
    node_id: randomUUID()
  });

  // Customer 2: Water Sector
  CREATE (c2:Customer {
    customer_id: 'CUST-002-WATER',
    customer_name: 'Metropolitan Water District',
    industry_sector: 'water',
    criticality_tier: 'Tier1',
    contract_start_date: date('2021-03-22'),
    contract_status: 'active',
    regulatory_requirements: ['EPA Safe Drinking Water Act', 'State Water Resources Control Board'],
    primary_contact_email: 'security@metrowater.example',
    created_date: datetime(),
    last_updated: datetime(),
    node_id: randomUUID()
  });

  // Customer 3: Manufacturing Sector
  CREATE (c3:Customer {
    customer_id: 'CUST-003-MFG',
    customer_name: 'Advanced Manufacturing Corp',
    industry_sector: 'manufacturing',
    criticality_tier: 'Tier2',
    contract_start_date: date('2022-06-10'),
    contract_status: 'active',
    regulatory_requirements: ['ISO 27001', 'NIST CSF', 'SOC 2 Type II'],
    primary_contact_email: 'it-security@advancedmfg.example',
    created_date: datetime(),
    last_updated: datetime(),
    node_id: randomUUID()
  });

  // Organization 1: Energy - SCADA Operations
  CREATE (o1:Organization {
    org_id: 'ORG-RPA-SCADA',
    org_name: 'SCADA Operations',
    parent_customer_id: 'CUST-001-ENERGY',
    org_type: 'operational_unit',
    location: 'Regional Control Center - Northeast',
    responsible_manager: 'Chief Operations Officer',
    budget_code: 'RPA-OPS-001',
    created_date: datetime(),
    last_updated: datetime(),
    node_id: randomUUID()
  });

  // Organization 2: Water - Treatment Facilities
  CREATE (o2:Organization {
    org_id: 'ORG-MWD-TREATMENT',
    org_name: 'Water Treatment Facilities',
    parent_customer_id: 'CUST-002-WATER',
    org_type: 'operational_unit',
    location: 'Central Treatment Plant',
    responsible_manager: 'Director of Operations',
    budget_code: 'MWD-TREAT-001',
    created_date: datetime(),
    last_updated: datetime(),
    node_id: randomUUID()
  });

  // Organization 3: Manufacturing - Assembly Line
  CREATE (o3:Organization {
    org_id: 'ORG-AMC-ASSEMBLY',
    org_name: 'Assembly Line Automation',
    parent_customer_id: 'CUST-003-MFG',
    org_type: 'production_unit',
    location: 'Factory Floor 3',
    responsible_manager: 'VP of Manufacturing',
    budget_code: 'AMC-PROD-003',
    created_date: datetime(),
    last_updated: datetime(),
    node_id: randomUUID()
  });

  // Create HAS_ORGANIZATION relationships
  MATCH (c1:Customer {customer_id: 'CUST-001-ENERGY'})
  MATCH (o1:Organization {org_id: 'ORG-RPA-SCADA'})
  CREATE (c1)-[:HAS_ORGANIZATION {relationship_created: datetime()}]->(o1);

  MATCH (c2:Customer {customer_id: 'CUST-002-WATER'})
  MATCH (o2:Organization {org_id: 'ORG-MWD-TREATMENT'})
  CREATE (c2)-[:HAS_ORGANIZATION {relationship_created: datetime()}]->(o2);

  MATCH (c3:Customer {customer_id: 'CUST-003-MFG'})
  MATCH (o3:Organization {org_id: 'ORG-AMC-ASSEMBLY'})
  CREATE (c3)-[:HAS_ORGANIZATION {relationship_created: datetime()}]->(o3);

  Verify Step 2:
  MATCH (c:Customer)
  OPTIONAL MATCH (c)-[:HAS_ORGANIZATION]->(o:Organization)
  RETURN
    count(DISTINCT c) AS customer_count,
    count(DISTINCT o) AS organization_count,
    collect(DISTINCT c.customer_name) AS customer_names;
  Expected: customer_count: 3, organization_count: 3

  Step 3: Assign Equipment to Customers (10 minutes)

  I recommend Option C: Even Distribution for testing (37-37-37 split):

  // Assign first 37 Equipment nodes to Customer 1 (Energy)
  MATCH (e:Equipment)
  WHERE e.customer_id IS NULL
  WITH e LIMIT 37
  SET e.customer_id = 'CUST-001-ENERGY',
      e.organization_id = 'ORG-RPA-SCADA',
      e.asset_owner = 'Regional Power Authority',
      e.ownership_status = 'active',
      e.shared_asset = false;

  // Assign next 37 to Customer 2 (Water)
  MATCH (e:Equipment)
  WHERE e.customer_id IS NULL
  WITH e LIMIT 37
  SET e.customer_id = 'CUST-002-WATER',
      e.organization_id = 'ORG-MWD-TREATMENT',
      e.asset_owner = 'Metropolitan Water District',
      e.ownership_status = 'active',
      e.shared_asset = false;

  // Assign remaining to Customer 3 (Manufacturing)
  MATCH (e:Equipment)
  WHERE e.customer_id IS NULL
  SET e.customer_id = 'CUST-003-MFG',
      e.organization_id = 'ORG-AMC-ASSEMBLY',
      e.asset_owner = 'Advanced Manufacturing Corp',
      e.ownership_status = 'active',
      e.shared_asset = false;

  CRITICAL Validation - CVE Preservation:
  // Verify NO CVEs were modified
  MATCH (cve:CVE)
  WHERE EXISTS(cve.customer_id)
  RETURN count(cve) AS incorrectly_modified_cves;
  MUST = 0 (if not 0, execute rollback immediately)

  Verify Step 3:
  MATCH (asset:Equipment)
  RETURN
    count(asset) AS total_equipment,
    count(asset.customer_id) AS assigned_count,
    count(asset) - count(asset.customer_id) AS unassigned_count;
  Expected: total_equipment: 111, assigned_count: 111, unassigned_count: 0

  Step 4: Create Ownership Relationships (5 minutes)

  // Create Customer → Equipment OWNS_EQUIPMENT relationships
  MATCH (c:Customer)
  MATCH (asset:Equipment)
  WHERE asset.customer_id = c.customer_id
    AND NOT EXISTS((c)-[:OWNS_EQUIPMENT]->(asset))
  CREATE (c)-[:OWNS_EQUIPMENT {
    acquired_date: date('2020-01-01'),
    warranty_expiration: date('2025-12-31'),
    asset_criticality: coalesce(asset.criticality_score, 50),
    ownership_type: CASE WHEN asset.shared_asset = true THEN 'shared' ELSE 'owned' END,
    maintenance_status: 'active',
    relationship_created: datetime()
  }]->(asset);

  // Create Organization → Equipment MANAGES_EQUIPMENT relationships
  MATCH (o:Organization)
  MATCH (asset:Equipment)
  WHERE asset.organization_id = o.org_id
    AND NOT EXISTS((o)-[:MANAGES_EQUIPMENT]->(asset))
  CREATE (o)-[:MANAGES_EQUIPMENT {
    responsible_team: 'IT Operations',
    maintenance_contract: 'Standard',
    budget_allocation: 'OpEx',
    relationship_created: datetime()
  }]->(asset);

  Verify Step 4:
  MATCH (c:Customer)-[owns:OWNS_EQUIPMENT]->(asset:Equipment)
  RETURN
    c.customer_name AS customer,
    count(DISTINCT asset) AS owned_equipment
  ORDER BY customer;
  Expected: 3 rows showing ~37 equipment each

  Step 5: Final Validation (10 minutes)

  Execute all critical validations:

  // 1. CVE Count Baseline
  MATCH (cve:CVE)
  RETURN count(cve) AS cve_count;
  // Document this number - should be 267,487

  // 2. CVE Integrity Check (CRITICAL)
  MATCH (cve:CVE)
  WHERE EXISTS(cve.customer_id) OR EXISTS(cve.organization_id) OR EXISTS(cve.asset_owner)
  RETURN count(cve) AS incorrectly_modified_cves;
  // MUST = 0

  // 3. Customer Filtering Test
  MATCH (c:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(asset)
  RETURN labels(asset)[0] AS asset_type, count(asset) AS my_equipment_count;
  // Should show Equipment: ~37

  // 4. Multi-Customer Isolation Test
  MATCH (c1:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(asset1)
  MATCH (c2:Customer {customer_id: 'CUST-002-WATER'})-[:OWNS_EQUIPMENT]->(asset2)
  WHERE asset1 = asset2 AND asset1.shared_asset <> true
  RETURN count(asset1) AS incorrectly_shared_assets;
  // MUST = 0

  // 5. Comprehensive Report
  CALL {
    MATCH (cve:CVE) RETURN count(cve) AS cve_count
  }
  CALL {
    MATCH (c:Customer) RETURN count(c) AS customer_count
  }
  CALL {
    MATCH (o:Organization) RETURN count(o) AS organization_count
  }
  CALL {
    MATCH (asset:Equipment)
    WHERE asset.customer_id IS NOT NULL
    RETURN count(asset) AS assigned_assets
  }
  CALL {
    MATCH (:Customer)-[r:OWNS_EQUIPMENT]->()
    RETURN count(r) AS ownership_relationships
  }
  RETURN cve_count, customer_count, organization_count, assigned_assets, ownership_relationships;

  Expected Final Report:
  - cve_count: 267,487
  - customer_count: 3
  - organization_count: 3
  - assigned_assets: 111
  - ownership_relationships: 111

  Test Customer Filtering Query

  Once Steps 1-5 complete successfully, test the customer filtering capability:

  // Question 1: Does CVE-2024-1234 impact MY equipment?
  MATCH (customer:Customer {customer_id: 'CUST-001-ENERGY'})-[:OWNS_EQUIPMENT]->(equipment:Equipment)
  MATCH (equipment)<-[:INSTALLED_ON]-(comp:SoftwareComponent)-[:HAS_VULNERABILITY]->(cve:CVE)
  WHERE cve.cve_id = 'CVE-2024-1234'  // Replace with actual CVE from your database
  RETURN
    equipment.type AS my_equipment,
    comp.name AS vulnerable_component,
    cve.cve_id AS cve_id,
    cve.cvss_base_score AS severity
  ORDER BY cve.cvss_base_score DESC;

  Files Created for Reference

  1. CUSTOMER_ORGANIZATION_IMPLEMENTATION.md - Complete implementation guide
  2. CUSTOMER_FILTERING_QUERY_EXAMPLES.md - All 8 questions with before/after examples
  3. STEP5_MANUAL_VALIDATION_GUIDE.md - Detailed validation procedures
  4. IMPLEMENTATION_STATUS_REPORT.md - This comprehensive status report

  All scripts are ready for copy-paste execution. The implementation will add customer labeling capability without modifying any of your 267,487 CVE nodes.

  Total Execution Time: 32-42 minutesRisk Level: LOW (all operations additive and reversible)