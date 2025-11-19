// ═══════════════════════════════════════════════════════════════════════════════
// COMMUNICATIONS SECTOR - VALIDATION QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

// 1. Facility Statistics
MATCH (f:Facility)
WHERE f.facilityId STARTS WITH 'FAC-COM-'
RETURN '=== FACILITY STATISTICS ===' as section, '' as detail
UNION
MATCH (f:Facility)
WHERE f.facilityId STARTS WITH 'FAC-COM-'
RETURN 'Total Facilities' as section, toString(count(f)) as detail
UNION
MATCH (f:Facility)
WHERE f.facilityId STARTS WITH 'FAC-COM-'
  AND f.latitude IS NOT NULL
RETURN 'Facilities with Coordinates' as section, toString(count(f)) as detail
UNION
MATCH (f:Facility)
WHERE f.facilityId STARTS WITH 'FAC-COM-'
RETURN 'Facility Types' as section, f.facilityType + ': ' + toString(count(*)) as detail
ORDER BY section, detail;

// 2. Equipment Statistics
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
RETURN '=== EQUIPMENT STATISTICS ===' as section, '' as detail
UNION
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
RETURN 'Total Equipment' as section, toString(count(eq)) as detail
UNION
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
RETURN 'Equipment Types' as section, eq.equipmentType + ': ' + toString(count(*)) as detail
ORDER BY section, detail;

// 3. Relationship Statistics
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'COM-'
RETURN '=== RELATIONSHIP STATISTICS ===' as section, '' as detail
UNION
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'COM-'
RETURN 'Total LOCATED_AT Relationships' as section, toString(count(r)) as detail
UNION
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
OPTIONAL MATCH (eq)-[r:LOCATED_AT]->(f:Facility)
WITH count(eq) as total, count(r) as linked
RETURN 'Relationship Coverage' as section, toString(linked) + '/' + toString(total) + ' (' + toString(round(100.0 * linked / total, 2)) + '%)' as detail
ORDER BY section, detail;

// 4. Tagging Statistics
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
  AND size(eq.tags) > 0
RETURN '=== TAGGING STATISTICS ===' as section, '' as detail
UNION
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
  AND size(eq.tags) > 0
RETURN 'Tagged Equipment' as section, toString(count(eq)) as detail
UNION
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
UNWIND eq.tags as tag
RETURN 'Tag Categories' as section, substring(tag, 0, 4) + '_*: ' + toString(count(*)) as detail
ORDER BY section, detail;

// 5. Geographic Distribution
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'COM-'
RETURN '=== GEOGRAPHIC DISTRIBUTION ===' as section, '' as detail
UNION
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'COM-'
RETURN 'By State' as section, f.state + ': ' + toString(count(eq)) + ' equipment' as detail
ORDER BY section, detail DESC;

// 6. CVE Preservation Validation
MATCH (n:CVE)
RETURN '=== BACKWARD COMPATIBILITY ===' as section, '' as detail
UNION
MATCH (n:CVE)
RETURN 'CVE Nodes Preserved' as section, toString(count(n)) as detail
ORDER BY section, detail;

// 7. Sample Data - Top 5 Facilities by Equipment Count
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'COM-'
WITH f, count(eq) as equipment_count
ORDER BY equipment_count DESC
LIMIT 5
RETURN '=== TOP 5 FACILITIES BY EQUIPMENT ===' as section, '' as detail
UNION
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'COM-'
WITH f, count(eq) as equipment_count
ORDER BY equipment_count DESC
LIMIT 5
RETURN f.facilityName as section, toString(equipment_count) + ' equipment (' + f.city + ', ' + f.state + ')' as detail
ORDER BY section, detail DESC;
