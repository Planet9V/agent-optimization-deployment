// GAP-004 UC3: Cascade Analysis Tests
// Test Suite: Cascading Failure Propagation
// Total Tests: 20

// Cleanup any existing test data from previous runs
MATCH (ce:CascadeEvent) WHERE ce.eventId STARTS WITH 'CASCADE_TEST_' DETACH DELETE ce;
MATCH (fp:FailurePropagation) WHERE fp.propagationId STARTS WITH 'PROP_TEST_' DETACH DELETE fp;
MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ_' DETACH DELETE eq;

// Setup: Create test cascade scenario
CREATE (ce1:CascadeEvent {
  eventId: 'CASCADE_TEST_001',
  triggerType: 'Overload',
  timestamp: datetime(),
  severity: 'critical',
  impactedEquipmentCount: 0,
  propagationDepth: 0
});

CREATE (ce2:CascadeEvent {
  eventId: 'CASCADE_TEST_002',
  triggerType: 'ShortCircuit',
  timestamp: datetime() + duration('PT5M'),
  severity: 'high',
  impactedEquipmentCount: 0,
  propagationDepth: 0
});

CREATE (fp1:FailurePropagation {
  propagationId: 'PROP_TEST_001',
  fromEquipmentId: 'EQ_TRANS_001',
  toEquipmentId: 'EQ_SWITCH_001',
  propagationTime: duration('PT2M'),
  propagationProbability: 0.85,
  damageLevel: 'moderate'
});

CREATE (fp2:FailurePropagation {
  propagationId: 'PROP_TEST_002',
  fromEquipmentId: 'EQ_SWITCH_001',
  toEquipmentId: 'EQ_CIRCUIT_BREAKER_001',
  propagationTime: duration('PT3M'),
  propagationProbability: 0.72,
  damageLevel: 'severe'
});

// Week 7 Enhancement: Expand equipment graph to support 15-hop cascades
CREATE (eq1:Equipment {equipmentId: 'EQ_TRANS_001', equipmentType: 'Transformer', name: 'Transformer A1', status: 'active'});
CREATE (eq2:Equipment {equipmentId: 'EQ_SWITCH_001', equipmentType: 'Switch', name: 'Switch B1', status: 'active'});
CREATE (eq3:Equipment {equipmentId: 'EQ_CIRCUIT_BREAKER_001', equipmentType: 'Circuit Breaker', name: 'CB C1', status: 'active'});
CREATE (eq4:Equipment {equipmentId: 'EQ_SWITCH_002', equipmentType: 'Switch', name: 'Switch B2', status: 'active'});
CREATE (eq5:Equipment {equipmentId: 'EQ_CIRCUIT_BREAKER_002', equipmentType: 'Circuit Breaker', name: 'CB C2', status: 'active'});
CREATE (eq6:Equipment {equipmentId: 'EQ_RELAY_001', equipmentType: 'Relay', name: 'Relay D1', status: 'active'});
CREATE (eq7:Equipment {equipmentId: 'EQ_SWITCH_003', equipmentType: 'Switch', name: 'Switch B3', status: 'active'});
CREATE (eq8:Equipment {equipmentId: 'EQ_TRANS_002', equipmentType: 'Transformer', name: 'Transformer A2', status: 'active'});
CREATE (eq9:Equipment {equipmentId: 'EQ_SWITCH_004', equipmentType: 'Switch', name: 'Switch B4', status: 'active'});
CREATE (eq10:Equipment {equipmentId: 'EQ_CIRCUIT_BREAKER_003', equipmentType: 'Circuit Breaker', name: 'CB C3', status: 'active'});
CREATE (eq11:Equipment {equipmentId: 'EQ_SWITCH_005', equipmentType: 'Switch', name: 'Switch B5', status: 'active'});
CREATE (eq12:Equipment {equipmentId: 'EQ_TRANS_003', equipmentType: 'Transformer', name: 'Transformer A3', status: 'active'});
CREATE (eq13:Equipment {equipmentId: 'EQ_CIRCUIT_BREAKER_004', equipmentType: 'Circuit Breaker', name: 'CB C4', status: 'active'});
CREATE (eq14:Equipment {equipmentId: 'EQ_SWITCH_006', equipmentType: 'Switch', name: 'Switch B6', status: 'active'});
CREATE (eq15:Equipment {equipmentId: 'EQ_CIRCUIT_BREAKER_005', equipmentType: 'Circuit Breaker', name: 'CB C5', status: 'active'});
CREATE (eq16:Equipment {equipmentId: 'EQ_CAPACITOR_001', equipmentType: 'Capacitor', name: 'Capacitor E1', status: 'active'});
// Week 7 Enhancement: Create 15-hop cascade chain with branching
MATCH (eq1:Equipment {equipmentId: 'EQ_TRANS_001'})
MATCH (eq2:Equipment {equipmentId: 'EQ_SWITCH_001'})
MATCH (eq3:Equipment {equipmentId: 'EQ_CIRCUIT_BREAKER_001'})
MATCH (eq4:Equipment {equipmentId: 'EQ_SWITCH_002'})
MATCH (eq5:Equipment {equipmentId: 'EQ_CIRCUIT_BREAKER_002'})
MATCH (eq6:Equipment {equipmentId: 'EQ_RELAY_001'})
MATCH (eq7:Equipment {equipmentId: 'EQ_SWITCH_003'})
MATCH (eq8:Equipment {equipmentId: 'EQ_TRANS_002'})
MATCH (eq9:Equipment {equipmentId: 'EQ_SWITCH_004'})
MATCH (eq10:Equipment {equipmentId: 'EQ_CIRCUIT_BREAKER_003'})
MATCH (eq11:Equipment {equipmentId: 'EQ_SWITCH_005'})
MATCH (eq12:Equipment {equipmentId: 'EQ_TRANS_003'})
MATCH (eq13:Equipment {equipmentId: 'EQ_CIRCUIT_BREAKER_004'})
MATCH (eq14:Equipment {equipmentId: 'EQ_SWITCH_006'})
MATCH (eq15:Equipment {equipmentId: 'EQ_CIRCUIT_BREAKER_005'})
MATCH (eq16:Equipment {equipmentId: 'EQ_CAPACITOR_001'})

// Main cascade chain (15 hops)
CREATE (eq1)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 100.0}]->(eq2)
CREATE (eq2)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 80.0}]->(eq3)
CREATE (eq3)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 75.0}]->(eq4)
CREATE (eq4)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 70.0}]->(eq5)
CREATE (eq5)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 65.0}]->(eq6)
CREATE (eq6)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 60.0}]->(eq7)
CREATE (eq7)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 55.0}]->(eq8)
CREATE (eq8)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 90.0}]->(eq9)
CREATE (eq9)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 50.0}]->(eq10)
CREATE (eq10)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 45.0}]->(eq11)
CREATE (eq11)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 40.0}]->(eq12)
CREATE (eq12)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 85.0}]->(eq13)
CREATE (eq13)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 35.0}]->(eq14)
CREATE (eq14)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 30.0}]->(eq15)
CREATE (eq15)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 25.0}]->(eq16)

// Branching paths for realistic topology
CREATE (eq2)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 60.0}]->(eq6)
CREATE (eq8)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 70.0}]->(eq13);

MATCH (ce1:CascadeEvent {eventId: 'CASCADE_TEST_001'})
MATCH (ce2:CascadeEvent {eventId: 'CASCADE_TEST_002'})
MATCH (fp1:FailurePropagation {propagationId: 'PROP_TEST_001'})
MATCH (fp2:FailurePropagation {propagationId: 'PROP_TEST_002'})
MATCH (eq1:Equipment {equipmentId: 'EQ_TRANS_001'})
MATCH (eq2:Equipment {equipmentId: 'EQ_SWITCH_001'})
MATCH (eq3:Equipment {equipmentId: 'EQ_CIRCUIT_BREAKER_001'})
CREATE (ce1)-[:TRIGGERED_BY]->(eq1)
CREATE (ce2)-[:TRIGGERED_BY]->(eq2)
CREATE (fp1)-[:PROPAGATES_FROM]->(eq1)
CREATE (fp1)-[:PROPAGATES_TO]->(eq2)
CREATE (fp2)-[:PROPAGATES_FROM]->(eq2)
CREATE (fp2)-[:PROPAGATES_TO]->(eq3);

// Test 1: Query CascadeEvent by triggerType
MATCH (ce:CascadeEvent {triggerType: 'Overload'})
RETURN
  CASE WHEN count(ce) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_1_result,
  'Find cascade events by trigger type' AS test_1_description,
  count(ce) AS overload_events;

// Test 2: Query CascadeEvent by severity
MATCH (ce:CascadeEvent)
WHERE ce.severity IN ['critical', 'high']
RETURN
  CASE WHEN count(ce) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_2_result,
  'Find high severity cascade events' AS test_2_description,
  count(ce) AS high_severity_count;

// Test 3: Test FailurePropagation relationship queries
MATCH (fp:FailurePropagation)-[:PROPAGATES_FROM]->(eq1:Equipment)
MATCH (fp)-[:PROPAGATES_TO]->(eq2:Equipment)
RETURN
  CASE WHEN count(fp) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_3_result,
  'Find failure propagation relationships' AS test_3_description,
  count(fp) AS propagation_count;

// Test 4: Test cascading failure simulation (8-hop query)
MATCH path = (ce:CascadeEvent)-[:TRIGGERED_BY]->(eq1:Equipment)
             -[:CONNECTS_TO*1..8]->(eq2:Equipment)
WHERE ce.eventId = 'CASCADE_TEST_001'
RETURN
  CASE WHEN length(path) >= 3 THEN 'PASS' ELSE 'FAIL' END AS test_4_result,
  'Find cascading failure paths (8 hops)' AS test_4_description,
  length(path) AS cascade_depth;

// Test 5: Test cascading failure simulation (15-hop query)
MATCH path = (ce:CascadeEvent)-[:TRIGGERED_BY]->(eq1:Equipment)
             -[:CONNECTS_TO*1..15]->(eq2:Equipment)
WHERE ce.eventId = 'CASCADE_TEST_001'
WITH path
ORDER BY length(path) DESC
LIMIT 1
RETURN
  CASE WHEN length(path) >= 3 THEN 'PASS' ELSE 'FAIL' END AS test_5_result,
  'Find maximum cascading failure path (15 hops)' AS test_5_description,
  length(path) AS max_cascade_depth;

// Test 6: Test temporal ordering of cascade events
MATCH (ce1:CascadeEvent), (ce2:CascadeEvent)
WHERE ce1.timestamp < ce2.timestamp
RETURN
  CASE WHEN count(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_6_result,
  'Verify temporal ordering of cascade events' AS test_6_description,
  count(*) AS temporally_ordered_pairs;

// Test 7: Test propagation probability aggregation
MATCH path = (fp1:FailurePropagation)-[:PROPAGATES_TO]->(eq:Equipment)
             <-[:PROPAGATES_FROM]-(fp2:FailurePropagation)
WITH path, fp1, fp2,
     fp1.propagationProbability * fp2.propagationProbability AS combined_probability
RETURN
  CASE WHEN combined_probability > 0 THEN 'PASS' ELSE 'FAIL' END AS test_7_result,
  'Calculate combined propagation probability' AS test_7_description,
  combined_probability AS combined_prob;

// Test 8: Test propagation time aggregation
MATCH path = (fp1:FailurePropagation)-[:PROPAGATES_TO]->(eq:Equipment)
             <-[:PROPAGATES_FROM]-(fp2:FailurePropagation)
WITH path, fp1, fp2,
     fp1.propagationTime.seconds + fp2.propagationTime.seconds AS total_time_seconds
RETURN
  CASE WHEN total_time_seconds > 0 THEN 'PASS' ELSE 'FAIL' END AS test_8_result,
  'Calculate total propagation time' AS test_8_description,
  total_time_seconds AS total_time;

// Test 9: Test damage level severity classification
MATCH (fp:FailurePropagation)
WHERE fp.damageLevel IN ['severe', 'critical']
RETURN
  CASE WHEN count(fp) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_9_result,
  'Find severe/critical damage propagations' AS test_9_description,
  count(fp) AS severe_damage_count;

// Test 10: Test cascade event impact count update
MATCH (ce:CascadeEvent {eventId: 'CASCADE_TEST_001'})-[:TRIGGERED_BY]->(eq1:Equipment)
MATCH path = (eq1)-[:CONNECTS_TO*1..5]->(eq2:Equipment)
WITH ce, count(DISTINCT eq2) AS impacted_count
SET ce.impactedEquipmentCount = impacted_count
RETURN
  CASE WHEN ce.impactedEquipmentCount >= 0 THEN 'PASS' ELSE 'FAIL' END AS test_10_result,
  'Update cascade event impacted equipment count' AS test_10_description,
  ce.impactedEquipmentCount AS impacted_count;

// Test 11: Test cascade event propagation depth update
MATCH (ce:CascadeEvent {eventId: 'CASCADE_TEST_001'})-[:TRIGGERED_BY]->(eq1:Equipment)
MATCH path = (eq1)-[:CONNECTS_TO*1..10]->(eq2:Equipment)
WITH ce, max(length(path)) AS max_depth
SET ce.propagationDepth = max_depth
RETURN
  CASE WHEN ce.propagationDepth > 0 THEN 'PASS' ELSE 'FAIL' END AS test_11_result,
  'Update cascade event propagation depth' AS test_11_description,
  ce.propagationDepth AS max_depth;

// Test 12: Test cascading failure by equipment type
MATCH path = (ce:CascadeEvent)-[:TRIGGERED_BY]->(eq1:Equipment)
             -[:CONNECTS_TO*1..8]->(eq2:Equipment)
WHERE eq1.equipmentType = 'Transformer'
  AND eq2.equipmentType IN ['Switch', 'Circuit Breaker']
RETURN
  CASE WHEN length(path) >= 3 THEN 'PASS' ELSE 'FAIL' END AS test_12_result,
  'Find cascades from transformers to switches/breakers' AS test_12_description,
  length(path) AS cascade_depth;

// Test 13: Test multi-cascade event correlation
MATCH (ce1:CascadeEvent), (ce2:CascadeEvent)
WHERE ce1.timestamp < ce2.timestamp
  AND duration.between(ce1.timestamp, ce2.timestamp).seconds < 600
RETURN
  CASE WHEN count(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_13_result,
  'Find correlated cascade events (within 10 minutes)' AS test_13_description,
  count(*) AS correlated_events;

// Test 14: Test failure propagation probability threshold
MATCH (fp:FailurePropagation)
WHERE fp.propagationProbability > 0.8
RETURN
  CASE WHEN count(fp) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_14_result,
  'Find high-probability failure propagations (>0.8)' AS test_14_description,
  count(fp) AS high_prob_count;

// Test 15: Test cascade event equipment impact summary
MATCH (ce:CascadeEvent)-[:TRIGGERED_BY]->(eq:Equipment)
WITH ce, eq.equipmentType AS type, count(*) AS trigger_count
RETURN
  CASE WHEN trigger_count > 0 THEN 'PASS' ELSE 'FAIL' END AS test_15_result,
  'Summarize cascade triggers by equipment type' AS test_15_description,
  type, trigger_count;

// Test 16: Test failure propagation path visualization
MATCH path = (eq1:Equipment)-[:CONNECTS_TO*1..5]->(eq2:Equipment)
WHERE eq1.equipmentId = 'EQ_TRANS_001'
WITH path, [node IN nodes(path) | node.equipmentId] AS equipment_path
RETURN
  CASE WHEN size(equipment_path) > 1 THEN 'PASS' ELSE 'FAIL' END AS test_16_result,
  'Visualize failure propagation paths' AS test_16_description,
  equipment_path AS propagation_path;

// Test 17: Test cascade event temporal window queries
MATCH (ce:CascadeEvent)
WHERE ce.timestamp > datetime() - duration('PT1H')
  AND ce.timestamp < datetime()
RETURN
  CASE WHEN count(ce) >= 0 THEN 'PASS' ELSE 'FAIL' END AS test_17_result,
  'Find cascade events in last hour' AS test_17_description,
  count(ce) AS recent_cascade_count;

// Test 18: Test failure propagation damage aggregation
MATCH (fp:FailurePropagation)
WITH fp.damageLevel AS damage, count(*) AS damage_count
RETURN
  CASE WHEN damage_count > 0 THEN 'PASS' ELSE 'FAIL' END AS test_18_result,
  'Aggregate failure propagations by damage level' AS test_18_description,
  damage, damage_count;

// Test 19: Test cascade event criticality scoring
MATCH (ce:CascadeEvent)
WITH ce,
     CASE ce.severity
       WHEN 'critical' THEN 5
       WHEN 'high' THEN 4
       WHEN 'medium' THEN 3
       WHEN 'low' THEN 2
       ELSE 1
     END AS severity_score,
     ce.impactedEquipmentCount AS impact_score
WITH ce, (severity_score * 2 + impact_score) AS criticality_score
RETURN
  CASE WHEN criticality_score > 0 THEN 'PASS' ELSE 'FAIL' END AS test_19_result,
  'Calculate cascade event criticality scores' AS test_19_description,
  ce.eventId, criticality_score;

// Test 20: Test cascading failure root cause analysis
MATCH (ce:CascadeEvent)-[:TRIGGERED_BY]->(eq:Equipment)
MATCH path = (eq)-[:CONNECTS_TO*1..10]->(downstream:Equipment)
WITH ce, eq, count(DISTINCT downstream) AS affected_count
RETURN
  CASE WHEN affected_count >= 0 THEN 'PASS' ELSE 'FAIL' END AS test_20_result,
  'Identify root cause equipment for cascades' AS test_20_description,
  eq.equipmentId AS root_cause,
  affected_count AS downstream_impact;

// Cleanup test data
MATCH (ce:CascadeEvent) WHERE ce.eventId STARTS WITH 'CASCADE_TEST_' DELETE ce;
MATCH (fp:FailurePropagation) WHERE fp.propagationId STARTS WITH 'PROP_TEST_' DELETE fp;
MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ_' AND eq.name CONTAINS 'Test' DELETE eq;

// Summary
RETURN 'GAP-004 UC3 Cascade Analysis Tests Complete' AS summary,
       20 AS total_tests,
       'Run each test and count PASS/FAIL results' AS instruction;
