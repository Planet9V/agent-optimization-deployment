// ═══════════════════════════════════════════════════════════════
// PHASE 1: Add Facility Layer (100% ADDITIVE)
// Universal Location Architecture Migration
// Created: 2025-11-13
// Status: READY FOR DEPLOYMENT
// Constitution: GAP-004 Zero Breaking Changes
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// CONSTRAINTS - Facility Layer
// ───────────────────────────────────────────────────────────────

// Facility uniqueness constraint
CREATE CONSTRAINT facility_id IF NOT EXISTS
FOR (f:Facility) REQUIRE f.facilityId IS UNIQUE;

// Customer uniqueness constraint
CREATE CONSTRAINT customer_id IF NOT EXISTS
FOR (c:Customer) REQUIRE c.customerId IS UNIQUE;

// Region uniqueness constraint
CREATE CONSTRAINT region_id IF NOT EXISTS
FOR (r:Region) REQUIRE r.regionId IS UNIQUE;

// Sector uniqueness constraint
CREATE CONSTRAINT sector_id IF NOT EXISTS
FOR (s:Sector) REQUIRE s.sectorId IS UNIQUE;

// ───────────────────────────────────────────────────────────────
// INDEXES - Performance Optimization
// ───────────────────────────────────────────────────────────────

// Facility indexes
CREATE INDEX facility_name IF NOT EXISTS
FOR (f:Facility) ON (f.name);

CREATE INDEX facility_type IF NOT EXISTS
FOR (f:Facility) ON (f.facilityType);

CREATE INDEX facility_namespace IF NOT EXISTS
FOR (f:Facility) ON (f.customer_namespace);

// Spatial index on Facility geographic properties
CREATE INDEX facility_location IF NOT EXISTS
FOR (f:Facility) ON (f.`geographic.latitude`, f.`geographic.longitude`);

// Tag indexes for flexible categorization
CREATE INDEX facility_tags IF NOT EXISTS
FOR (f:Facility) ON (f.tags);

// Customer indexes
CREATE INDEX customer_name IF NOT EXISTS
FOR (c:Customer) ON (c.name);

CREATE INDEX customer_namespace IF NOT EXISTS
FOR (c:Customer) ON (c.customer_namespace);

// Region indexes
CREATE INDEX region_name IF NOT EXISTS
FOR (r:Region) ON (r.name);

CREATE INDEX region_type IF NOT EXISTS
FOR (r:Region) ON (r.regionType);

// Sector indexes
CREATE INDEX sector_name IF NOT EXISTS
FOR (s:Sector) ON (s.name);

CREATE INDEX sector_critical IF NOT EXISTS
FOR (s:Sector) ON (s.criticalInfrastructure);

// ───────────────────────────────────────────────────────────────
// VALIDATION - Verify Existing Schema Untouched
// ───────────────────────────────────────────────────────────────

// Verify existing Equipment nodes accessible (should return count)
MATCH (eq:Equipment) RETURN count(eq) AS equipment_count;

// Verify existing constraints operational (should return >= 129)
SHOW CONSTRAINTS YIELD name RETURN count(name) AS constraint_count;

// Verify existing indexes operational (should return >= 455)
SHOW INDEXES YIELD name RETURN count(name) AS index_count;

// ───────────────────────────────────────────────────────────────
// COMPLETION MESSAGE
// ───────────────────────────────────────────────────────────────

// Phase 1 Complete: Facility Layer constraints and indexes added
// Zero existing nodes/relationships/properties deleted
// Ready for Phase 2: Add Relationships
