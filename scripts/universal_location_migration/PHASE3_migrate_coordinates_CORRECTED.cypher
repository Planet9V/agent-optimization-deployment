// ============================================================================
// PHASE 3: Migrate Equipment Coordinates to Facility-based Architecture
// CORRECTED VERSION: Extract facility name from location string
// ============================================================================

// Step 1: Create LOCATED_AT relationships (Equipment → Facility)
// Extract facility prefix from Equipment.location and match to Facility.name
MATCH (e:Equipment), (f:Facility)
WHERE e.location IS NOT NULL 
  AND e.location STARTS WITH f.name
MERGE (e)-[r:LOCATED_AT]->(f)
SET r.created_at = datetime(),
    r.migration_phase = 'PHASE3',
    r.source = 'location_string_extraction';

// Step 2: Create bidirectional HOUSES_EQUIPMENT relationships
MATCH (e:Equipment)-[:LOCATED_AT]->(f:Facility)
MERGE (f)-[r:HOUSES_EQUIPMENT]->(e)
SET r.created_at = datetime(),
    r.migration_phase = 'PHASE3';

// Step 3: Verification Queries
MATCH ()-[r:LOCATED_AT]->() 
RETURN 'LOCATED_AT relationships created' as status, count(r) as count;

MATCH ()-[r:HOUSES_EQUIPMENT]->() 
RETURN 'HOUSES_EQUIPMENT relationships created' as status, count(r) as count;

MATCH (e:Equipment) 
OPTIONAL MATCH (e)-[:LOCATED_AT]->(f:Facility)
RETURN 'Equipment with facility relationships' as status, 
       count(DISTINCT e) as total_equipment, 
       count(DISTINCT f) as equipment_with_facility,
       (count(DISTINCT f) * 100.0 / count(DISTINCT e)) as percentage;

// Verify Equipment.location preserved
MATCH (e:Equipment) 
WHERE e.location IS NULL 
RETURN 'Equipment without location string' as status, count(e) as count;
