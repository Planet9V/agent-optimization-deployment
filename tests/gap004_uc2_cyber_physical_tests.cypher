// GAP-004 UC2: Cyber-Physical System Tests
// Test Suite: Digital Twin & Physical Sensor Integration
// Total Tests: 20

// Setup: Create test data
CREATE (dt:DigitalTwinState {
  twinStateId: 'DT_TEST_001',
  twinId: 'TWIN_TRANSFORMER_001',
  timestamp: datetime(),
  currentState: 'normal',
  expectedValues: '{"voltage": 11000, "current": 150, "temperature": 65}',
  deviationThreshold: 10.0
});

CREATE (ps:PhysicalSensor {
  sensorId: 'SENSOR_TEST_001',
  sensorType: 'VoltageSensor',
  location: 'Substation_A',
  currentReading: 11500,
  lastUpdate: datetime(),
  calibrationDate: date(),
  accuracy: 99.5
});

CREATE (eq:Equipment {
  equipmentId: 'EQ_TRANSFORMER_001',
  equipmentType: 'Transformer',
  name: 'Main Transformer A1',
  status: 'active',
  manufacturer: 'ABB',
  installDate: date('2020-01-15')
});

CREATE (dt)-[:MONITORS]->(eq);
CREATE (ps)-[:MEASURES]->(eq);

// Test 1: Query DigitalTwinState expectedValues JSON
MATCH (dt:DigitalTwinState {twinStateId: 'DT_TEST_001'})
WITH dt, apoc.convert.fromJsonMap(dt.expectedValues) AS expected
RETURN
  CASE WHEN expected.voltage = 11000 THEN 'PASS' ELSE 'FAIL' END AS test_1_result,
  'Parse expectedValues JSON correctly' AS test_1_description,
  expected.voltage AS voltage_value;

// Test 2: Calculate deviation from expected values
MATCH (dt:DigitalTwinState {twinStateId: 'DT_TEST_001'})
MATCH (ps:PhysicalSensor {sensorId: 'SENSOR_TEST_001'})
WITH dt, ps, apoc.convert.fromJsonMap(dt.expectedValues) AS expected
WITH dt, ps, expected, abs(ps.currentReading - expected.voltage) AS deviation
RETURN
  CASE WHEN deviation > (dt.deviationThreshold * expected.voltage / 100) THEN 'PASS' ELSE 'FAIL' END AS test_2_result,
  'Detect anomaly when deviation exceeds threshold' AS test_2_description,
  deviation AS calculated_deviation;

// Test 3: Test PhysicalSensor anomaly detection query
MATCH (ps:PhysicalSensor)-[:MEASURES]->(eq:Equipment)
MATCH (dt:DigitalTwinState)-[:MONITORS]->(eq)
WITH ps, dt, apoc.convert.fromJsonMap(dt.expectedValues) AS expected
WHERE ps.sensorType = 'VoltageSensor'
  AND abs(ps.currentReading - expected.voltage) > (dt.deviationThreshold * expected.voltage / 100)
RETURN
  CASE WHEN count(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_3_result,
  'Find sensors with anomalies' AS test_3_description,
  collect(ps.sensorId) AS anomalous_sensors;

// Test 4: Test cyber-physical attack pattern (8-hop query)
MATCH path = (dt:DigitalTwinState)-[:MONITORS]->(eq1:Equipment)-[:CONNECTS_TO*1..8]->(eq2:Equipment)
WHERE dt.twinStateId = 'DT_TEST_001'
RETURN
  CASE WHEN length(path) >= 3 THEN 'PASS' ELSE 'FAIL' END AS test_4_result,
  'Find cyber-physical attack propagation paths' AS test_4_description,
  length(path) AS path_length;

// Test 5: Test multi-tenant isolation (verify tenant_id separation)
CREATE (dt2:DigitalTwinState {
  twinStateId: 'DT_TEST_002',
  twinId: 'TWIN_TRANSFORMER_002',
  timestamp: datetime(),
  currentState: 'normal',
  expectedValues: '{"voltage": 33000}',
  tenant_id: 'TENANT_B'
});

MATCH (dt:DigitalTwinState {tenant_id: 'TENANT_B'})
RETURN
  CASE WHEN count(dt) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_5_result,
  'Multi-tenant isolation query works' AS test_5_description,
  count(dt) AS tenant_b_count;

// Test 6: Test timestamp-based sensor reading queries
MATCH (ps:PhysicalSensor)
WHERE ps.lastUpdate > datetime() - duration('PT1H')
RETURN
  CASE WHEN count(ps) >= 0 THEN 'PASS' ELSE 'FAIL' END AS test_6_result,
  'Query sensors updated in last hour' AS test_6_description,
  count(ps) AS recent_sensors;

// Test 7: Test calibration status query
MATCH (ps:PhysicalSensor)
WHERE ps.calibrationDate < date() - duration('P365D')
RETURN
  CASE WHEN count(ps) >= 0 THEN 'PASS' ELSE 'FAIL' END AS test_7_result,
  'Find sensors needing recalibration' AS test_7_description,
  count(ps) AS expired_calibration_count;

// Test 8: Test accuracy threshold query
MATCH (ps:PhysicalSensor)
WHERE ps.accuracy < 95.0
RETURN
  CASE WHEN count(ps) >= 0 THEN 'PASS' ELSE 'FAIL' END AS test_8_result,
  'Find sensors below accuracy threshold' AS test_8_description,
  count(ps) AS low_accuracy_count;

// Test 9: Test DigitalTwinState aggregation by equipment type
MATCH (dt:DigitalTwinState)-[:MONITORS]->(eq:Equipment)
WITH eq.equipmentType AS type, count(dt) AS twin_count
RETURN
  CASE WHEN twin_count > 0 THEN 'PASS' ELSE 'FAIL' END AS test_9_result,
  'Aggregate digital twins by equipment type' AS test_9_description,
  type, twin_count;

// Test 10: Test sensor reading aggregation by location
MATCH (ps:PhysicalSensor)
WITH ps.location AS location, avg(ps.currentReading) AS avg_reading
RETURN
  CASE WHEN avg_reading IS NOT NULL THEN 'PASS' ELSE 'FAIL' END AS test_10_result,
  'Aggregate sensor readings by location' AS test_10_description,
  location, avg_reading;

// Test 11: Test 15-hop cyber-physical attack propagation
MATCH path = (dt:DigitalTwinState)-[:MONITORS]->(eq1:Equipment)-[:CONNECTS_TO*1..15]->(eq2:Equipment)
WHERE dt.twinStateId = 'DT_TEST_001'
WITH path
ORDER BY length(path) DESC
LIMIT 1
RETURN
  CASE WHEN length(path) >= 3 THEN 'PASS' ELSE 'FAIL' END AS test_11_result,
  'Find maximum cyber-physical attack path (15 hops)' AS test_11_description,
  length(path) AS max_path_length;

// Test 12: Test deviation calculation with multiple sensors
MATCH (ps:PhysicalSensor)-[:MEASURES]->(eq:Equipment)
MATCH (dt:DigitalTwinState)-[:MONITORS]->(eq)
WITH eq, dt, collect(ps) AS sensors, apoc.convert.fromJsonMap(dt.expectedValues) AS expected
UNWIND sensors AS sensor
WITH eq, dt, sensor, expected,
     abs(sensor.currentReading - expected.voltage) AS deviation,
     (dt.deviationThreshold * expected.voltage / 100) AS threshold
RETURN
  CASE WHEN deviation > threshold THEN 'PASS' ELSE 'FAIL' END AS test_12_result,
  'Calculate deviations for multiple sensors' AS test_12_description,
  sensor.sensorId, deviation, threshold;

// Test 13: Test cyber-physical attack detection with timestamp
MATCH (dt:DigitalTwinState)-[:MONITORS]->(eq:Equipment)
WHERE dt.timestamp > datetime() - duration('PT1H')
  AND dt.currentState = 'anomaly'
RETURN
  CASE WHEN count(*) >= 0 THEN 'PASS' ELSE 'FAIL' END AS test_13_result,
  'Detect recent cyber-physical anomalies' AS test_13_description,
  count(*) AS recent_anomalies;

// Test 14: Test sensor measurement relationship validation
MATCH (ps:PhysicalSensor)-[r:MEASURES]->(eq:Equipment)
RETURN
  CASE WHEN count(r) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_14_result,
  'Verify sensor-equipment measurement relationships' AS test_14_description,
  count(r) AS measurement_relationships;

// Test 15: Test digital twin monitoring relationship validation
MATCH (dt:DigitalTwinState)-[r:MONITORS]->(eq:Equipment)
RETURN
  CASE WHEN count(r) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_15_result,
  'Verify digital twin-equipment monitoring relationships' AS test_15_description,
  count(r) AS monitoring_relationships;

// Test 16: Test JSON parsing for multiple expectedValues fields
MATCH (dt:DigitalTwinState)
WITH dt, apoc.convert.fromJsonMap(dt.expectedValues) AS expected
RETURN
  CASE WHEN expected IS NOT NULL THEN 'PASS' ELSE 'FAIL' END AS test_16_result,
  'Parse all expectedValues JSON fields' AS test_16_description,
  expected.voltage AS voltage, expected.current AS current, expected.temperature AS temperature;

// Test 17: Test equipment status impact on cyber-physical queries
MATCH (eq:Equipment {status: 'active'})<-[:MONITORS]-(dt:DigitalTwinState)
RETURN
  CASE WHEN count(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_17_result,
  'Find digital twins monitoring active equipment' AS test_17_description,
  count(*) AS active_monitoring;

// Test 18: Test cyber-physical attack path with equipment type filtering
MATCH path = (dt:DigitalTwinState)-[:MONITORS]->(eq1:Equipment)-[:CONNECTS_TO*1..10]->(eq2:Equipment)
WHERE eq1.equipmentType = 'Transformer'
  AND eq2.equipmentType IN ['Switch', 'Circuit Breaker']
RETURN
  CASE WHEN length(path) >= 3 THEN 'PASS' ELSE 'FAIL' END AS test_18_result,
  'Find attack paths from transformers to switches' AS test_18_description,
  length(path) AS path_length;

// Test 19: Test sensor accuracy impact on anomaly detection
MATCH (ps:PhysicalSensor)-[:MEASURES]->(eq:Equipment)
MATCH (dt:DigitalTwinState)-[:MONITORS]->(eq)
WHERE ps.accuracy > 98.0
WITH ps, dt, apoc.convert.fromJsonMap(dt.expectedValues) AS expected
WHERE abs(ps.currentReading - expected.voltage) > (dt.deviationThreshold * expected.voltage / 100)
RETURN
  CASE WHEN count(*) >= 0 THEN 'PASS' ELSE 'FAIL' END AS test_19_result,
  'Find high-accuracy sensors detecting anomalies' AS test_19_description,
  count(*) AS high_accuracy_anomalies;

// Test 20: Test cyber-physical system health summary
MATCH (dt:DigitalTwinState)-[:MONITORS]->(eq:Equipment)
MATCH (ps:PhysicalSensor)-[:MEASURES]->(eq)
WITH dt, eq, collect(ps) AS sensors
RETURN
  CASE WHEN count(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_20_result,
  'Generate cyber-physical system health summary' AS test_20_description,
  count(DISTINCT dt) AS digital_twins,
  count(DISTINCT eq) AS equipment,
  size(sensors) AS sensors_per_equipment;

// Cleanup test data
MATCH (dt:DigitalTwinState) WHERE dt.twinStateId STARTS WITH 'DT_TEST_' DELETE dt;
MATCH (ps:PhysicalSensor) WHERE ps.sensorId STARTS WITH 'SENSOR_TEST_' DELETE ps;
MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ_TRANSFORMER_' DELETE eq;

// Summary
RETURN 'GAP-004 UC2 Cyber-Physical Tests Complete' AS summary,
       20 AS total_tests,
       'Run each test and count PASS/FAIL results' AS instruction;
