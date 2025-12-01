// Level 5 Integration Tests - Testing Cross-Level Relationships
// Generated: 2025-11-23
// Database: OpenSPG Neo4j

// ============================================================================
// TEST 1: InformationEvent → CVE Links (316K CVEs)
// ============================================================================

// Test 1.1: Count InformationEvents linked to CVEs
MATCH (ie:InformationEvent)-[r:REFERENCES|MENTIONS|DESCRIBES]->(cve:CVE)
RETURN
  'TEST_1.1_InformationEvent_to_CVE' as test_name,
  count(DISTINCT ie) as information_events,
  count(DISTINCT cve) as cves_referenced,
  count(r) as total_links,
  collect(DISTINCT type(r))[0..5] as relationship_types
LIMIT 1;

// Test 1.2: Sample InformationEvents with CVE references
MATCH (ie:InformationEvent)-[r]->(cve:CVE)
RETURN
  'TEST_1.2_Sample_IE_CVE_Links' as test_name,
  ie.id as event_id,
  ie.title as event_title,
  type(r) as relationship,
  cve.id as cve_id,
  cve.cvss_score as cvss_score
LIMIT 10;

// Test 1.3: CVEs by severity linked to InformationEvents
MATCH (ie:InformationEvent)-[r]->(cve:CVE)
WHERE cve.cvss_score IS NOT NULL
WITH
  CASE
    WHEN cve.cvss_score >= 9.0 THEN 'CRITICAL'
    WHEN cve.cvss_score >= 7.0 THEN 'HIGH'
    WHEN cve.cvss_score >= 4.0 THEN 'MEDIUM'
    ELSE 'LOW'
  END as severity,
  count(DISTINCT cve) as cve_count,
  count(DISTINCT ie) as event_count
RETURN
  'TEST_1.3_CVE_Severity_Distribution' as test_name,
  severity,
  cve_count,
  event_count
ORDER BY
  CASE severity
    WHEN 'CRITICAL' THEN 1
    WHEN 'HIGH' THEN 2
    WHEN 'MEDIUM' THEN 3
    ELSE 4
  END;

// ============================================================================
// TEST 2: Event → Sector Links (16 sectors)
// ============================================================================

// Test 2.1: Events by sector
MATCH (e:Event)
WHERE e.sector IS NOT NULL
RETURN
  'TEST_2.1_Events_By_Sector' as test_name,
  e.sector as sector,
  count(e) as event_count
ORDER BY event_count DESC;

// Test 2.2: InformationEvents by sector with CVE links
MATCH (ie:InformationEvent)-[r]->(cve:CVE)
WHERE ie.sector IS NOT NULL
RETURN
  'TEST_2.2_IE_Sector_CVE_Links' as test_name,
  ie.sector as sector,
  count(DISTINCT ie) as events,
  count(DISTINCT cve) as cves,
  avg(toFloat(cve.cvss_score)) as avg_cvss_score
ORDER BY events DESC;

// Test 2.3: Critical infrastructure sectors with high-severity CVEs
MATCH (ie:InformationEvent)-[r]->(cve:CVE)
WHERE ie.sector IS NOT NULL
  AND cve.cvss_score >= 7.0
RETURN
  'TEST_2.3_Critical_Sectors_High_CVEs' as test_name,
  ie.sector as sector,
  count(DISTINCT cve) as high_severity_cves,
  count(DISTINCT ie) as events,
  max(toFloat(cve.cvss_score)) as max_cvss_score
ORDER BY high_severity_cves DESC
LIMIT 10;

// ============================================================================
// TEST 3: Event → Device Links (50K devices)
// ============================================================================

// Test 3.1: Device types in database
MATCH (d)
WHERE any(label in labels(d) WHERE label CONTAINS 'Device' OR label CONTAINS 'Equipment')
RETURN
  'TEST_3.1_Device_Types' as test_name,
  labels(d) as device_labels,
  count(d) as device_count
ORDER BY device_count DESC
LIMIT 15;

// Test 3.2: Events affecting devices by sector
MATCH (e:Event)-[r:AFFECTS|IMPACTS|TARGETS]->(d)
WHERE any(label in labels(d) WHERE label CONTAINS 'Device' OR label CONTAINS 'Equipment')
  AND e.sector IS NOT NULL
RETURN
  'TEST_3.2_Events_Affecting_Devices' as test_name,
  e.sector as sector,
  count(DISTINCT e) as events,
  count(DISTINCT d) as devices_affected,
  collect(DISTINCT type(r))[0..3] as relationship_types
ORDER BY devices_affected DESC
LIMIT 10;

// Test 3.3: Devices with CVE vulnerabilities
MATCH (cve:CVE)<-[r1]-(ie:InformationEvent)-[r2:AFFECTS|IMPACTS|TARGETS]->(d)
WHERE any(label in labels(d) WHERE label CONTAINS 'Device' OR label CONTAINS 'Equipment')
RETURN
  'TEST_3.3_Devices_With_CVE_Vulnerabilities' as test_name,
  labels(d) as device_type,
  count(DISTINCT d) as devices,
  count(DISTINCT cve) as cves,
  count(DISTINCT ie) as events,
  avg(toFloat(cve.cvss_score)) as avg_cvss_score
ORDER BY devices DESC
LIMIT 10;

// ============================================================================
// TEST 4: Bias → Decision Links
// ============================================================================

// Test 4.1: Cognitive biases in database
MATCH (b:CognitiveBias)
RETURN
  'TEST_4.1_Cognitive_Biases' as test_name,
  count(b) as bias_count,
  collect(b.name)[0..10] as sample_biases
LIMIT 1;

// Test 4.2: Decisions influenced by biases
MATCH (b:CognitiveBias)-[r:INFLUENCES|AFFECTS]->(d:Decision)
RETURN
  'TEST_4.2_Bias_Decision_Links' as test_name,
  b.name as bias_name,
  count(DISTINCT d) as decisions_influenced,
  collect(DISTINCT type(r))[0..3] as relationship_types
ORDER BY decisions_influenced DESC
LIMIT 10;

// Test 4.3: Decision patterns by bias category
MATCH (b:CognitiveBias)-[r]->(d:Decision)
WHERE b.category IS NOT NULL
RETURN
  'TEST_4.3_Decision_Patterns_By_Bias_Category' as test_name,
  b.category as bias_category,
  count(DISTINCT b) as biases,
  count(DISTINCT d) as decisions,
  count(r) as total_influences
ORDER BY decisions DESC;

// ============================================================================
// TEST 5: Cross-Level Query Performance
// ============================================================================

// Test 5.1: Multi-hop path - Bias → Decision → Event → CVE
MATCH path = (b:CognitiveBias)-[:INFLUENCES|AFFECTS*1..2]->(d:Decision)-[:RESULTS_IN|LEADS_TO*1..2]->(e:Event)-[:REFERENCES|MENTIONS]->(cve:CVE)
RETURN
  'TEST_5.1_Multi_Hop_Bias_to_CVE' as test_name,
  count(path) as paths_found,
  avg(length(path)) as avg_path_length,
  min(length(path)) as min_path_length,
  max(length(path)) as max_path_length
LIMIT 1;

// Test 5.2: Sector impact analysis - Events → Devices → CVEs
MATCH (e:Event)-[r1:AFFECTS|IMPACTS]->(d)-[r2]-(cve:CVE)
WHERE any(label in labels(d) WHERE label CONTAINS 'Device' OR label CONTAINS 'Equipment')
  AND e.sector IS NOT NULL
RETURN
  'TEST_5.2_Sector_Device_CVE_Impact' as test_name,
  e.sector as sector,
  count(DISTINCT d) as devices_impacted,
  count(DISTINCT cve) as cves_involved,
  count(DISTINCT e) as events,
  avg(toFloat(cve.cvss_score)) as avg_cvss_score
ORDER BY devices_impacted DESC
LIMIT 10;

// Test 5.3: Full stack query - Bias → Decision → Event → Device → CVE
MATCH (b:CognitiveBias)-[:INFLUENCES*1..2]->(d:Decision)-[:RESULTS_IN*1..2]->(e:Event)-[:AFFECTS*1..2]->(dev)-[r]-(cve:CVE)
WHERE any(label in labels(dev) WHERE label CONTAINS 'Device' OR label CONTAINS 'Equipment')
  AND cve.cvss_score >= 7.0
RETURN
  'TEST_5.3_Full_Stack_High_Severity' as test_name,
  b.name as bias,
  count(DISTINCT e) as events,
  count(DISTINCT dev) as devices,
  count(DISTINCT cve) as high_severity_cves,
  avg(toFloat(cve.cvss_score)) as avg_cvss_score
ORDER BY high_severity_cves DESC
LIMIT 10;

// ============================================================================
// TEST 6: Performance Benchmarks
// ============================================================================

// Test 6.1: Node count by level
MATCH (n)
RETURN
  'TEST_6.1_Node_Count_By_Level' as test_name,
  CASE
    WHEN 'CognitiveBias' IN labels(n) THEN 'Level_1_Bias'
    WHEN 'Decision' IN labels(n) THEN 'Level_2_Decision'
    WHEN 'Event' IN labels(n) OR 'InformationEvent' IN labels(n) THEN 'Level_3_Event'
    WHEN any(label in labels(n) WHERE label CONTAINS 'Device' OR label CONTAINS 'Equipment') THEN 'Level_4_Device'
    WHEN 'CVE' IN labels(n) THEN 'Level_5_CVE'
    ELSE 'Other'
  END as level,
  count(n) as node_count
ORDER BY level;

// Test 6.2: Relationship count by type
MATCH ()-[r]->()
RETURN
  'TEST_6.2_Relationship_Count_By_Type' as test_name,
  type(r) as relationship_type,
  count(r) as relationship_count
ORDER BY relationship_count DESC
LIMIT 20;

// Test 6.3: Database statistics
CALL db.stats.retrieve('GRAPH COUNTS') YIELD data
RETURN
  'TEST_6.3_Database_Statistics' as test_name,
  data.nodes as total_nodes,
  data.relationships as total_relationships,
  data.relTypesCount as relationship_types,
  data.labelCount as label_count;

// ============================================================================
// END OF TESTS
// ============================================================================
