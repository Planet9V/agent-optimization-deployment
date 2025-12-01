// ═══════════════════════════════════════════════════════════════
// GAP-004 HEALTHCARE SECTOR DEPLOYMENT - COMPLETION SCRIPT
// ═══════════════════════════════════════════════════════════════
// Date: 2025-11-19
// Purpose: Complete Healthcare sector deployment
//   - Add missing 60th facility (DC Medical Center)
//   - Update all 60 facilities with Healthcare sector tag
//   - Verify all relationships and tagging
// ═══════════════════════════════════════════════════════════════

// STEP 1: Add missing DC Medical Center facility
CREATE (f:Facility {
  facilityId: 'HEALTH-DC-MED-001',
  name: 'Washington DC Medical Center',
  facilityType: 'Medical Center',
  address: '1100 23rd Street NW',
  city: 'Washington',
  state: 'DC',
  zip_code: '20037',
  country: 'USA',
  location: point({latitude: 38.9072, longitude: -77.0469}),
  sector: 'Healthcare',
  operational_status: 'active',
  capacity: 350,
  tags: ['HEALTH_FACILITY', 'SECTOR_HEALTHCARE', 'GEO_REGION_NORTHEAST', 'GEO_STATE_DC', 'OPS_FACILITY_MEDICAL_CENTER'],
  created_date: datetime(),
  updated_date: datetime()
});

// STEP 2: Update all 59 existing facilities with Healthcare sector tag
MATCH (f:Facility)
WHERE f.facilityId STARTS WITH 'HEALTH-'
  AND NOT EXISTS(f.sector)
SET f.sector = 'Healthcare',
    f.tags = CASE
      WHEN f.tags IS NULL THEN ['HEALTH_FACILITY', 'SECTOR_HEALTHCARE']
      WHEN NOT 'SECTOR_HEALTHCARE' IN f.tags THEN f.tags + ['SECTOR_HEALTHCARE']
      ELSE f.tags
    END,
    f.updated_date = datetime()
RETURN count(f) as updated_facilities;

// STEP 3: Verify facility count
MATCH (f:Facility {sector: 'Healthcare'})
RETURN count(f) as total_healthcare_facilities;

// STEP 4: Verify equipment count
MATCH (e:Equipment)
WHERE e.equipmentId STARTS WITH 'EQ-HEALTH-'
RETURN count(e) as total_healthcare_equipment;

// STEP 5: Verify relationships
MATCH (e:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE e.equipmentId STARTS WITH 'EQ-HEALTH-'
  AND f.sector = 'Healthcare'
RETURN count(r) as total_relationships,
       count(DISTINCT e) as unique_equipment,
       count(DISTINCT f) as unique_facilities;

// STEP 6: Verify tagging completeness
MATCH (e:Equipment)
WHERE e.equipmentId STARTS WITH 'EQ-HEALTH-'
WITH e, size(e.tags) as tag_count
RETURN min(tag_count) as min_tags,
       max(tag_count) as max_tags,
       avg(tag_count) as avg_tags,
       count(e) as total_equipment;

// STEP 7: Get sample of facilities by type
MATCH (f:Facility {sector: 'Healthcare'})
RETURN f.facilityType as type, count(f) as count
ORDER BY count DESC;

// STEP 8: Get sample of equipment by type
MATCH (e:Equipment)
WHERE e.equipmentId STARTS WITH 'EQ-HEALTH-'
RETURN e.equipmentType as type, count(e) as count
ORDER BY count DESC;

// STEP 9: Verify geographic distribution
MATCH (f:Facility {sector: 'Healthcare'})
RETURN f.state as state, count(f) as facility_count
ORDER BY facility_count DESC;

// STEP 10: Verify tag dimensions
MATCH (e:Equipment)
WHERE e.equipmentId STARTS WITH 'EQ-HEALTH-'
UNWIND e.tags as tag
WITH tag
WHERE tag STARTS WITH 'GEO_' OR tag STARTS WITH 'OPS_' OR tag STARTS WITH 'REG_' OR tag STARTS WITH 'TECH_' OR tag STARTS WITH 'TIME_'
RETURN split(tag, '_')[0] as dimension, count(DISTINCT tag) as unique_tags
ORDER BY dimension;
