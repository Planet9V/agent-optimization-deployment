// ============================================================
// CUSTOMER_LABELS: Multi-Tenant Isolation Schema
// Phase B1 - Order 1 of 6 MVP Enhancements
// Version: 1.0.0
// Created: 2025-12-04
// Purpose: Define customer isolation schema for all 189,932 entities
// ============================================================

// ------------------------------------------------------------
// SECTION 1: CustomerLabel Node Type
// ------------------------------------------------------------

// 1.1 Create CustomerLabel constraint (extends existing Customer)
CREATE CONSTRAINT customer_label_id IF NOT EXISTS
FOR (c:CustomerLabel) REQUIRE c.customer_id IS UNIQUE;

// 1.2 Unique namespace constraint
CREATE CONSTRAINT customer_namespace_unique IF NOT EXISTS
FOR (c:CustomerLabel) REQUIRE c.namespace IS UNIQUE;

// 1.3 Index on customer name for search
CREATE INDEX customer_label_name_idx IF NOT EXISTS
FOR (c:CustomerLabel) ON (c.name);

// 1.4 Index on customer status for filtering
CREATE INDEX customer_label_status_idx IF NOT EXISTS
FOR (c:CustomerLabel) ON (c.status);

// 1.5 Index on industry sector (for sector-specific analytics)
CREATE INDEX customer_label_sector_idx IF NOT EXISTS
FOR (c:CustomerLabel) ON (c.sector);

// ------------------------------------------------------------
// SECTION 2: customer_id Property Indexes (All Node Types)
// ------------------------------------------------------------

// Core entity types with customer isolation
CREATE INDEX entity_customer_idx IF NOT EXISTS
FOR (n:Entity) ON (n.customer_id);

CREATE INDEX cve_customer_idx IF NOT EXISTS
FOR (n:CVE) ON (n.customer_id);

CREATE INDEX cpe_customer_idx IF NOT EXISTS
FOR (n:CPE) ON (n.customer_id);

CREATE INDEX cwe_customer_idx IF NOT EXISTS
FOR (n:CWE) ON (n.customer_id);

CREATE INDEX asset_customer_idx IF NOT EXISTS
FOR (n:Asset) ON (n.customer_id);

CREATE INDEX threat_actor_customer_idx IF NOT EXISTS
FOR (n:ThreatActor) ON (n.customer_id);

CREATE INDEX technique_customer_idx IF NOT EXISTS
FOR (n:Technique) ON (n.customer_id);

CREATE INDEX capec_customer_idx IF NOT EXISTS
FOR (n:CAPEC) ON (n.customer_id);

CREATE INDEX software_customer_idx IF NOT EXISTS
FOR (n:Software) ON (n.customer_id);

CREATE INDEX organization_customer_idx IF NOT EXISTS
FOR (n:Organization) ON (n.customer_id);

CREATE INDEX document_customer_idx IF NOT EXISTS
FOR (n:Document) ON (n.customer_id);

// Composite indexes for common queries
CREATE INDEX cve_customer_severity_idx IF NOT EXISTS
FOR (n:CVE) ON (n.customer_id, n.cvssV3Severity);

CREATE INDEX asset_customer_type_idx IF NOT EXISTS
FOR (n:Asset) ON (n.customer_id, n.asset_type);

// ------------------------------------------------------------
// SECTION 3: Default Customer Creation
// ------------------------------------------------------------

// Create default system customer for shared data (CVEs, CWEs, CAPECs)
MERGE (c:CustomerLabel {customer_id: 'SYSTEM'})
ON CREATE SET
  c.name = 'System (Shared Data)',
  c.namespace = 'system',
  c.status = 'ACTIVE',
  c.created_at = datetime(),
  c.updated_at = datetime(),
  c.sector = 'GLOBAL',
  c.description = 'Shared data accessible to all customers (CVEs, CWEs, CAPECs, Techniques)',
  c.metadata = {
    is_system: true,
    allow_read_all: true,
    allow_write_admin_only: true
  };

// Create default customer for unassigned entities (migration)
MERGE (c:CustomerLabel {customer_id: 'DEFAULT'})
ON CREATE SET
  c.name = 'Default Customer',
  c.namespace = 'default',
  c.status = 'ACTIVE',
  c.created_at = datetime(),
  c.updated_at = datetime(),
  c.sector = 'UNASSIGNED',
  c.description = 'Default customer for entities pending assignment';

// ------------------------------------------------------------
// SECTION 4: BELONGS_TO_CUSTOMER Relationship Type
// ------------------------------------------------------------

// Note: Relationships don't have indexes, but we define the schema here
// Relationship: (Entity)-[:BELONGS_TO_CUSTOMER]->(CustomerLabel)
// Properties:
//   - assigned_at: datetime
//   - assigned_by: string (user/system ID)
//   - assignment_type: EXPLICIT | INHERITED | MIGRATION

// ------------------------------------------------------------
// VERIFICATION QUERIES
// ------------------------------------------------------------

// Verify constraints created
// SHOW CONSTRAINTS WHERE name CONTAINS 'customer'
// YIELD name, type, entityType, properties
// RETURN name, type, entityType, properties;

// Verify indexes created
// SHOW INDEXES WHERE name CONTAINS 'customer'
// YIELD name, type, labelsOrTypes, properties, state
// RETURN name, type, labelsOrTypes, properties, state;

// Count CustomerLabel nodes
// MATCH (c:CustomerLabel) RETURN count(c) AS customer_count;

// ============================================================
// END OF SCHEMA DEFINITION
// ============================================================
