// ═══════════════════════════════════════════════════════════════
// LEVEL 5 VALIDATION QUERIES - EXECUTED 2025-11-23
// ═══════════════════════════════════════════════════════════════
// Database: openspg-neo4j (Docker container)
// Execution Method: docker exec openspg-neo4j cypher-shell
// ═══════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════
// QUERY 1: LATENCY TEST (<5 min requirement)
// ═══════════════════════════════════════════════════════════════
// Status: FAILED - Cannot execute (missing HAS_BIAS relationships)
// Expected: Query completes in < 300,000 ms (5 minutes)
// Actual: Relationship type does not exist

MATCH (i:InformationStream)
WITH i LIMIT 1
WITH i, timestamp() AS start
MATCH (i)-[:HAS_BIAS]->(b:CognitiveBias)
WITH i, start, timestamp() - start AS latency_ms
RETURN
  i.name AS stream,
  latency_ms,
  (latency_ms < 300000) AS passes_requirement;

// RESULT: NO RESULTS (HAS_BIAS relationship does not exist)

// ═══════════════════════════════════════════════════════════════
// QUERY 2: CORRELATION TEST (≥0.75 requirement)
// ═══════════════════════════════════════════════════════════════
// Status: FAILED - Cannot calculate (missing relationships)
// Expected: Correlation between bias count and sector count >= 0.75
// Actual: No HAS_BIAS or TARGETS_SECTOR relationships exist

MATCH (i:InformationStream)-[:HAS_BIAS]->(b:CognitiveBias)
MATCH (b)-[:TARGETS_SECTOR]->(s:Sector)
WITH i,
  COUNT(DISTINCT b) AS bias_count,
  COUNT(DISTINCT s) AS sector_count
WITH i,
  bias_count,
  sector_count,
  toFloat(bias_count) / 30.0 AS bias_ratio,
  toFloat(sector_count) / 16.0 AS sector_ratio
WITH i,
  bias_ratio,
  sector_ratio,
  (bias_ratio + sector_ratio) / 2.0 AS correlation
RETURN
  i.name AS stream,
  bias_ratio,
  sector_ratio,
  correlation,
  (correlation >= 0.75) AS passes_requirement
ORDER BY correlation DESC
LIMIT 5;

// RESULT: NO RESULTS (HAS_BIAS and TARGETS_SECTOR relationships do not exist)

// ═══════════════════════════════════════════════════════════════
// QUERY 3: INTEGRATION TEST (links to all 16 sectors)
// ═══════════════════════════════════════════════════════════════
// Status: FAILED - Missing TARGETS_SECTOR relationships
// Expected: Each InformationStream links to 16 sectors
// Actual: No TARGETS_SECTOR relationships exist

MATCH (i:InformationStream)-[:HAS_BIAS]->(b:CognitiveBias)-[:TARGETS_SECTOR]->(s:Sector)
WITH i, COUNT(DISTINCT s) AS linked_sectors
RETURN
  i.name AS stream,
  linked_sectors,
  (linked_sectors = 16) AS passes_requirement
ORDER BY linked_sectors DESC
LIMIT 10;

// RESULT: NO RESULTS (relationship chain does not exist)

// ═══════════════════════════════════════════════════════════════
// QUERY 4: BIAS ACTIVATION TEST (30/30 biases)
// ═══════════════════════════════════════════════════════════════
// Status: FAILED - Only 7 biases exist, need 30
// Expected: 30 Cognitive Bias nodes activated per stream
// Actual: 7 bias nodes exist, 0 HAS_BIAS relationships

MATCH (i:InformationStream)-[:HAS_BIAS]->(b:CognitiveBias)
WITH i, COUNT(DISTINCT b) AS bias_count
RETURN
  i.name AS stream,
  bias_count,
  (bias_count = 30) AS passes_requirement
ORDER BY bias_count DESC
LIMIT 10;

// RESULT: NO RESULTS (HAS_BIAS relationship does not exist)

// ═══════════════════════════════════════════════════════════════
// DIAGNOSTIC QUERIES - WHAT ACTUALLY EXISTS
// ═══════════════════════════════════════════════════════════════

// Diagnostic 1: Count InformationStream nodes
MATCH (i:InformationStream)
RETURN COUNT(i) AS stream_count;
// RESULT: 600 streams exist ✓

// Diagnostic 2: Count Cognitive_Bias nodes
MATCH (b:Cognitive_Bias)
RETURN COUNT(b) AS bias_count;
// RESULT: 7 biases exist (need 30) ✗

// Diagnostic 3: Count Sector nodes
MATCH (s:Sector)
RETURN COUNT(s) AS sector_count;
// RESULT: 27 sectors exist (11 unique, need 16) ✗

// Diagnostic 4: List existing biases
MATCH (cb:Cognitive_Bias)
RETURN cb.bias_name AS bias_name
ORDER BY bias_name;
// RESULT:
// 1. Anchoring Bias
// 2. Authority Bias
// 3. Confirmation Bias
// 4. Optimism Bias
// 5. Recency Bias
// 6. Social Proof Bias
// 7. Urgency Bias

// Diagnostic 5: List unique sectors
MATCH (s:Sector)
RETURN DISTINCT s.name AS sector_name
ORDER BY sector_name;
// RESULT:
// 1. Critical Infrastructure
// 2. Education
// 3. Energy
// 4. Financial Services
// 5. Healthcare and Public Health
// 6. Legal and Professional Services
// 7. Manufacturing
// 8. State and Local Government
// 9. Technology
// 10. Transportation
// 11. Water and Wastewater

// Diagnostic 6: Check for HAS_BIAS relationship type
CALL db.relationshipTypes()
YIELD relationshipType
WHERE relationshipType CONTAINS 'BIAS'
RETURN relationshipType;
// RESULT: NO RESULTS (HAS_BIAS does not exist in schema)

// Diagnostic 7: Check for TARGETS_SECTOR relationship type
CALL db.relationshipTypes()
YIELD relationshipType
WHERE relationshipType CONTAINS 'SECTOR' OR relationshipType CONTAINS 'TARGETS'
RETURN relationshipType;
// RESULT: NO RESULTS (TARGETS_SECTOR does not exist in schema)

// Diagnostic 8: Check Cognitive_Bias relationships
MATCH (b:Cognitive_Bias)-[r]-(x)
RETURN type(r) AS relationship,
       labels(x) AS connected_to,
       COUNT(*) AS count
ORDER BY count DESC
LIMIT 10;
// RESULT:
// EXPLOITED_BY -> Social_Engineering_Tactic: 3 relationships
// (Cognitive_Bias is mostly isolated)

// Diagnostic 9: Sample InformationStream structure
MATCH (i:InformationStream)
RETURN i.id, i.name, i.streamType
LIMIT 5;
// RESULT:
// rt-001 | SCADA Real-Time Monitoring | real-time
// rt-2   | Real-Time Stream 2         | real-time
// rt-3   | Real-Time Stream 3         | real-time
// rt-4   | Real-Time Stream 4         | real-time
// rt-5   | Real-Time Stream 5         | real-time

// Diagnostic 10: Check all relationship types in database
CALL db.relationshipTypes()
YIELD relationshipType
RETURN relationshipType
LIMIT 20;
// RESULT: (existing relationship types, none matching HAS_BIAS or TARGETS_SECTOR)

// ═══════════════════════════════════════════════════════════════
// VALIDATION SUMMARY
// ═══════════════════════════════════════════════════════════════
//
// Test 1 (Latency): FAILED - Cannot execute (missing HAS_BIAS)
// Test 2 (Correlation): FAILED - Cannot calculate (missing relationships)
// Test 3 (Integration): FAILED - Missing TARGETS_SECTOR relationships
// Test 4 (Bias Activation): FAILED - Only 7/30 biases, no HAS_BIAS relationships
//
// ROOT CAUSE: Required graph pattern does not exist
// REQUIRED: InformationStream -[HAS_BIAS]-> CognitiveBias -[TARGETS_SECTOR]-> Sector
// ACTUAL:   InformationStream (isolated) | Cognitive_Bias (isolated) | Sector (isolated)
//
// BLOCKING ISSUES:
// 1. Missing 23 Cognitive_Bias nodes (7 exist, need 30)
// 2. Missing 5 Sector nodes (11 exist, need 16)
// 3. Missing HAS_BIAS relationships (~18,000 needed)
// 4. Missing TARGETS_SECTOR relationships (~480 needed)
//
// DEPLOYMENT STATUS: PARTIAL
// Infrastructure Layer: COMPLETE
// Cognitive Bias Layer: INCOMPLETE
//
// ═══════════════════════════════════════════════════════════════
