// ═══════════════════════════════════════════════════════════════════════
// GAP-004 WEEK 7: MISSING BASE ONTOLOGY CONSTRAINTS
// ═══════════════════════════════════════════════════════════════════════
// File: gap004_missing_base_constraints.cypher
// Created: 2025-11-13
// Purpose: Create unique constraints for base ontology nodes missing from original schema
// Discovery: Schema validation tests revealed Equipment, Asset, Component lack unique constraints
// Constitution: 100% ADDITIVE - adding constraints, not deleting
// ═══════════════════════════════════════════════════════════════════════

// Equipment - Critical infrastructure equipment nodes
CREATE CONSTRAINT equipment_id IF NOT EXISTS
FOR (n:Equipment) REQUIRE n.equipmentId IS UNIQUE;

// Asset - Asset tracking and management
CREATE CONSTRAINT asset_id IF NOT EXISTS
FOR (n:Asset) REQUIRE n.assetId IS UNIQUE;

// Component - System component nodes
CREATE CONSTRAINT component_id IF NOT EXISTS
FOR (n:Component) REQUIRE n.componentId IS UNIQUE;

// Note: Location constraint exists but uses 'id' property, not 'locationId'
// Existing: cybersec_location_id on Location.id
// Test expects locationId property - this is a test data issue, not constraint issue

// ═══════════════════════════════════════════════════════════════════════
// CONSTRAINT SUMMARY
// ═══════════════════════════════════════════════════════════════════════
// Total New Constraints: 3
// Constitution Impact: ADDITIVE (129 → 132 constraints)
// Breaking Changes: ZERO
// ═══════════════════════════════════════════════════════════════════════
