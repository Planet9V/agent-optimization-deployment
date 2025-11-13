// GAP-004 Sample Data: UC2 Cyber-Physical Attack Detection
// File: gap004_sample_data_uc2.cypher
// Created: 2025-11-13
// Purpose: Realistic test data for UC2 nodes (5 types, 10+ samples each)

// ==============================================================================
// UC2 Node Type 1: DigitalTwinState (10 samples)
// ==============================================================================

// Sample 1: Railway PLC Digital Twin - Normal Operation
CREATE (dt1:DigitalTwinState {
  stateId: "dt-state-plc-rail-001-20251113150000",
  assetId: "device-plc-rail-001",
  expectedValues: {
    temperature: 85.5,
    pressure: 120.3,
    flowRate: 450.0,
    valvePosition: 75,
    actuatorCommand: "OPEN"
  },
  timestamp: datetime('2025-11-13T15:00:00Z'),
  confidence: 0.95,
  physicsModel: "THERMODYNAMIC",
  modelVersion: "2.1.3",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Centrifuge Digital Twin - Nuclear Facility
CREATE (dt2:DigitalTwinState {
  stateId: "dt-state-centrifuge-001-20251113150100",
  assetId: "device-centrifuge-001",
  expectedValues: {
    rotationSpeed: 1064,
    temperature: 35.5,
    vibration: 2.3,
    bearingTemp: 42.0
  },
  timestamp: datetime('2025-11-13T15:01:00Z'),
  confidence: 0.98,
  physicsModel: "MECHANICAL",
  modelVersion: "3.2.1",
  customer_namespace: "customer:NuclearFacility-Alpha",
  is_shared: false
});

// Sample 3: Water Treatment Pump - SCADA System
CREATE (dt3:DigitalTwinState {
  stateId: "dt-state-pump-water-001-20251113150200",
  assetId: "device-pump-water-001",
  expectedValues: {
    flowRate: 850.0,
    pressure: 95.2,
    motorCurrent: 23.5,
    pumpSpeed: 1750
  },
  timestamp: datetime('2025-11-13T15:02:00Z'),
  confidence: 0.92,
  physicsModel: "FLUID_DYNAMICS",
  modelVersion: "1.8.7",
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 4: Electrical Substation Transformer
CREATE (dt4:DigitalTwinState {
  stateId: "dt-state-transformer-001-20251113150300",
  assetId: "device-transformer-001",
  expectedValues: {
    voltage: 138000,
    current: 450.0,
    temperature: 78.5,
    oilLevel: 95.0
  },
  timestamp: datetime('2025-11-13T15:03:00Z'),
  confidence: 0.94,
  physicsModel: "ELECTRICAL",
  modelVersion: "2.4.0",
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// Sample 5: Industrial Furnace - Manufacturing
CREATE (dt5:DigitalTwinState {
  stateId: "dt-state-furnace-001-20251113150400",
  assetId: "device-furnace-001",
  expectedValues: {
    temperature: 1250.0,
    pressure: 1.02,
    oxygenLevel: 18.5,
    fuelFlowRate: 120.0
  },
  timestamp: datetime('2025-11-13T15:04:00Z'),
  confidence: 0.89,
  physicsModel: "THERMODYNAMIC",
  modelVersion: "1.5.2",
  customer_namespace: "customer:SteelMill-Delta",
  is_shared: false
});

// Sample 6: HVAC System - Building Automation
CREATE (dt6:DigitalTwinState {
  stateId: "dt-state-hvac-001-20251113150500",
  assetId: "device-hvac-001",
  expectedValues: {
    temperature: 21.5,
    humidity: 45.0,
    airFlowRate: 3500.0,
    damperPosition: 60
  },
  timestamp: datetime('2025-11-13T15:05:00Z'),
  confidence: 0.87,
  physicsModel: "THERMODYNAMIC",
  modelVersion: "2.0.1",
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 7: Gas Pipeline Compressor
CREATE (dt7:DigitalTwinState {
  stateId: "dt-state-compressor-001-20251113150600",
  assetId: "device-compressor-001",
  expectedValues: {
    inletPressure: 850.0,
    outletPressure: 1200.0,
    temperature: 95.0,
    vibration: 3.5
  },
  timestamp: datetime('2025-11-13T15:06:00Z'),
  confidence: 0.93,
  physicsModel: "FLUID_DYNAMICS",
  modelVersion: "2.2.4",
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// Sample 8: Railway Signal Controller
CREATE (dt8:DigitalTwinState {
  stateId: "dt-state-signal-001-20251113150700",
  assetId: "device-signal-controller-001",
  expectedValues: {
    signalState: "GREEN",
    voltage: 24.0,
    current: 0.8,
    lampIntensity: 95.0
  },
  timestamp: datetime('2025-11-13T15:07:00Z'),
  confidence: 0.96,
  physicsModel: "ELECTRICAL",
  modelVersion: "1.9.0",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 9: Chemical Reactor - Process Control
CREATE (dt9:DigitalTwinState {
  stateId: "dt-state-reactor-001-20251113150800",
  assetId: "device-reactor-001",
  expectedValues: {
    temperature: 185.0,
    pressure: 12.5,
    stirrerSpeed: 350,
    ph: 7.2
  },
  timestamp: datetime('2025-11-13T15:08:00Z'),
  confidence: 0.91,
  physicsModel: "HYBRID",
  modelVersion: "3.0.0",
  customer_namespace: "customer:ChemPlant-Eta",
  is_shared: false
});

// Sample 10: Wind Turbine - Energy Generation
CREATE (dt10:DigitalTwinState {
  stateId: "dt-state-turbine-001-20251113150900",
  assetId: "device-turbine-001",
  expectedValues: {
    rotorSpeed: 12.5,
    powerOutput: 2500.0,
    windSpeed: 15.0,
    pitch: 8.5
  },
  timestamp: datetime('2025-11-13T15:09:00Z'),
  confidence: 0.88,
  physicsModel: "MECHANICAL",
  modelVersion: "2.3.1",
  customer_namespace: "customer:WindFarm-Theta",
  is_shared: false
});

// ==============================================================================
// UC2 Node Type 2: PhysicalSensor (10 samples)
// ==============================================================================

// Sample 1: Temperature Sensor - Railway PLC
CREATE (sensor1:PhysicalSensor {
  sensorId: "sensor-temp-plc001-01",
  sensorType: "TEMPERATURE",
  reading: 87.3,
  unit: "°C",
  timestamp: datetime('2025-11-13T15:00:05Z'),
  quality: "GOOD",
  assetId: "device-plc-rail-001",
  calibrationDate: date('2025-09-15'),
  calibrationDue: date('2026-09-15'),
  alarmThresholds: {
    lowLow: 60.0,
    low: 70.0,
    high: 95.0,
    highHigh: 105.0
  },
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Rotation Speed Sensor - Centrifuge (ANOMALOUS)
CREATE (sensor2:PhysicalSensor {
  sensorId: "sensor-speed-centrifuge001-01",
  sensorType: "ROTATION_SPEED",
  reading: 1410,
  unit: "RPM",
  timestamp: datetime('2025-11-13T15:01:05Z'),
  quality: "GOOD",
  assetId: "device-centrifuge-001",
  calibrationDate: date('2025-08-20'),
  calibrationDue: date('2026-08-20'),
  alarmThresholds: {
    lowLow: 800.0,
    low: 900.0,
    high: 1200.0,
    highHigh: 1300.0
  },
  customer_namespace: "customer:NuclearFacility-Alpha",
  is_shared: false
});

// Sample 3: Flow Rate Sensor - Water Pump
CREATE (sensor3:PhysicalSensor {
  sensorId: "sensor-flow-pump001-01",
  sensorType: "FLOW_RATE",
  reading: 848.5,
  unit: "L/min",
  timestamp: datetime('2025-11-13T15:02:05Z'),
  quality: "GOOD",
  assetId: "device-pump-water-001",
  calibrationDate: date('2025-07-10'),
  calibrationDue: date('2026-07-10'),
  alarmThresholds: {
    lowLow: 500.0,
    low: 600.0,
    high: 1000.0,
    highHigh: 1100.0
  },
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 4: Voltage Sensor - Transformer
CREATE (sensor4:PhysicalSensor {
  sensorId: "sensor-voltage-transformer001-01",
  sensorType: "VOLTAGE",
  reading: 137850.0,
  unit: "V",
  timestamp: datetime('2025-11-13T15:03:05Z'),
  quality: "GOOD",
  assetId: "device-transformer-001",
  calibrationDate: date('2025-10-01'),
  calibrationDue: date('2026-10-01'),
  alarmThresholds: {
    lowLow: 125000.0,
    low: 130000.0,
    high: 145000.0,
    highHigh: 150000.0
  },
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// Sample 5: Pressure Sensor - Industrial Furnace (STALE)
CREATE (sensor5:PhysicalSensor {
  sensorId: "sensor-pressure-furnace001-01",
  sensorType: "PRESSURE",
  reading: 1.02,
  unit: "atm",
  timestamp: datetime('2025-11-13T14:54:05Z'),
  quality: "STALE",
  assetId: "device-furnace-001",
  calibrationDate: date('2025-06-15'),
  calibrationDue: date('2026-06-15'),
  alarmThresholds: {
    lowLow: 0.8,
    low: 0.9,
    high: 1.2,
    highHigh: 1.3
  },
  customer_namespace: "customer:SteelMill-Delta",
  is_shared: false
});

// Sample 6: Humidity Sensor - HVAC
CREATE (sensor6:PhysicalSensor {
  sensorId: "sensor-humidity-hvac001-01",
  sensorType: "HUMIDITY",
  reading: 47.2,
  unit: "%",
  timestamp: datetime('2025-11-13T15:05:05Z'),
  quality: "GOOD",
  assetId: "device-hvac-001",
  calibrationDate: date('2025-09-01'),
  calibrationDue: date('2026-09-01'),
  alarmThresholds: {
    lowLow: 20.0,
    low: 30.0,
    high: 60.0,
    highHigh: 70.0
  },
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 7: Vibration Sensor - Gas Compressor
CREATE (sensor7:PhysicalSensor {
  sensorId: "sensor-vibration-compressor001-01",
  sensorType: "VIBRATION",
  reading: 3.7,
  unit: "Hz",
  timestamp: datetime('2025-11-13T15:06:05Z'),
  quality: "UNCERTAIN",
  assetId: "device-compressor-001",
  calibrationDate: date('2025-08-10'),
  calibrationDue: date('2026-08-10'),
  alarmThresholds: {
    lowLow: 0.0,
    low: 1.0,
    high: 5.0,
    highHigh: 7.0
  },
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// Sample 8: Current Sensor - Signal Controller
CREATE (sensor8:PhysicalSensor {
  sensorId: "sensor-current-signal001-01",
  sensorType: "CURRENT",
  reading: 0.82,
  unit: "A",
  timestamp: datetime('2025-11-13T15:07:05Z'),
  quality: "GOOD",
  assetId: "device-signal-controller-001",
  calibrationDate: date('2025-10-15'),
  calibrationDue: date('2026-10-15'),
  alarmThresholds: {
    lowLow: 0.3,
    low: 0.5,
    high: 1.2,
    highHigh: 1.5
  },
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 9: pH Sensor - Chemical Reactor
CREATE (sensor9:PhysicalSensor {
  sensorId: "sensor-ph-reactor001-01",
  sensorType: "LEVEL",
  reading: 7.15,
  unit: "pH",
  timestamp: datetime('2025-11-13T15:08:05Z'),
  quality: "GOOD",
  assetId: "device-reactor-001",
  calibrationDate: date('2025-07-20'),
  calibrationDue: date('2026-07-20'),
  alarmThresholds: {
    lowLow: 6.0,
    low: 6.5,
    high: 8.0,
    highHigh: 8.5
  },
  customer_namespace: "customer:ChemPlant-Eta",
  is_shared: false
});

// Sample 10: Position Sensor - Wind Turbine
CREATE (sensor10:PhysicalSensor {
  sensorId: "sensor-position-turbine001-01",
  sensorType: "POSITION",
  reading: 8.3,
  unit: "degrees",
  timestamp: datetime('2025-11-13T15:09:05Z'),
  quality: "GOOD",
  assetId: "device-turbine-001",
  calibrationDate: date('2025-09-25'),
  calibrationDue: date('2026-09-25'),
  alarmThresholds: {
    lowLow: 0.0,
    low: 2.0,
    high: 15.0,
    highHigh: 20.0
  },
  customer_namespace: "customer:WindFarm-Theta",
  is_shared: false
});

// ==============================================================================
// UC2 Node Type 3: PhysicalActuator (10 samples)
// ==============================================================================

// Sample 1: Valve Actuator - Railway PLC
CREATE (actuator1:PhysicalActuator {
  actuatorId: "actuator-valve-plc001-01",
  actuatorType: "VALVE",
  command: "OPEN",
  position: 75.5,
  feedback: "CONFIRMED",
  timestamp: datetime('2025-11-13T15:00:06Z'),
  assetId: "device-plc-rail-001",
  responseTime: duration('PT2.5S'),
  failSafeState: "CLOSED",
  controlMode: "AUTOMATIC",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Motor Actuator - Centrifuge
CREATE (actuator2:PhysicalActuator {
  actuatorId: "actuator-motor-centrifuge001-01",
  actuatorType: "MOTOR",
  command: "SPEED_75",
  position: 75.0,
  feedback: "CONFIRMED",
  timestamp: datetime('2025-11-13T15:01:06Z'),
  assetId: "device-centrifuge-001",
  responseTime: duration('PT1.8S'),
  failSafeState: "LAST_KNOWN",
  controlMode: "AUTOMATIC",
  customer_namespace: "customer:NuclearFacility-Alpha",
  is_shared: false
});

// Sample 3: Pump Actuator - Water Treatment
CREATE (actuator3:PhysicalActuator {
  actuatorId: "actuator-pump-water001-01",
  actuatorType: "PUMP",
  command: "START",
  position: 100.0,
  feedback: "CONFIRMED",
  timestamp: datetime('2025-11-13T15:02:06Z'),
  assetId: "device-pump-water-001",
  responseTime: duration('PT3.2S'),
  failSafeState: "CLOSED",
  controlMode: "AUTOMATIC",
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 4: Breaker Actuator - Transformer (FAILED)
CREATE (actuator4:PhysicalActuator {
  actuatorId: "actuator-breaker-transformer001-01",
  actuatorType: "BREAKER",
  command: "CLOSE",
  position: 0.0,
  feedback: "FAILED",
  timestamp: datetime('2025-11-13T15:03:06Z'),
  assetId: "device-transformer-001",
  responseTime: duration('PT5.0S'),
  failSafeState: "OPEN",
  controlMode: "MANUAL",
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// Sample 5: Damper Actuator - HVAC
CREATE (actuator5:PhysicalActuator {
  actuatorId: "actuator-damper-hvac001-01",
  actuatorType: "DAMPER",
  command: "AUTO",
  position: 60.0,
  feedback: "IN_PROGRESS",
  timestamp: datetime('2025-11-13T15:05:06Z'),
  assetId: "device-hvac-001",
  responseTime: duration('PT4.1S'),
  failSafeState: "OPEN",
  controlMode: "AUTOMATIC",
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 6: Valve Actuator - Gas Compressor
CREATE (actuator6:PhysicalActuator {
  actuatorId: "actuator-valve-compressor001-01",
  actuatorType: "VALVE",
  command: "OPEN",
  position: 85.0,
  feedback: "CONFIRMED",
  timestamp: datetime('2025-11-13T15:06:06Z'),
  assetId: "device-compressor-001",
  responseTime: duration('PT2.0S'),
  failSafeState: "CLOSED",
  controlMode: "AUTOMATIC",
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// Sample 7: Relay Actuator - Signal Controller
CREATE (actuator7:PhysicalActuator {
  actuatorId: "actuator-relay-signal001-01",
  actuatorType: "RELAY",
  command: "ON",
  position: 100.0,
  feedback: "CONFIRMED",
  timestamp: datetime('2025-11-13T15:07:06Z'),
  assetId: "device-signal-controller-001",
  responseTime: duration('PT0.5S'),
  failSafeState: "OFF",
  controlMode: "AUTOMATIC",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 8: Motor Actuator - Chemical Reactor Stirrer
CREATE (actuator8:PhysicalActuator {
  actuatorId: "actuator-motor-reactor001-01",
  actuatorType: "MOTOR",
  command: "SPEED_50",
  position: 50.0,
  feedback: "MISMATCH",
  timestamp: datetime('2025-11-13T15:08:06Z'),
  assetId: "device-reactor-001",
  responseTime: duration('PT3.5S'),
  failSafeState: "STOP",
  controlMode: "CASCADE",
  customer_namespace: "customer:ChemPlant-Eta",
  is_shared: false
});

// Sample 9: Heater Actuator - Furnace
CREATE (actuator9:PhysicalActuator {
  actuatorId: "actuator-heater-furnace001-01",
  actuatorType: "HEATER",
  command: "ON",
  position: 100.0,
  feedback: "CONFIRMED",
  timestamp: datetime('2025-11-13T15:04:06Z'),
  assetId: "device-furnace-001",
  responseTime: duration('PT6.0S'),
  failSafeState: "OFF",
  controlMode: "AUTOMATIC",
  customer_namespace: "customer:SteelMill-Delta",
  is_shared: false
});

// Sample 10: Motor Actuator - Wind Turbine Pitch
CREATE (actuator10:PhysicalActuator {
  actuatorId: "actuator-motor-turbine001-01",
  actuatorType: "MOTOR",
  command: "AUTO",
  position: 8.3,
  feedback: "CONFIRMED",
  timestamp: datetime('2025-11-13T15:09:06Z'),
  assetId: "device-turbine-001",
  responseTime: duration('PT2.8S'),
  failSafeState: "AS_IS",
  controlMode: "AUTOMATIC",
  customer_namespace: "customer:WindFarm-Theta",
  is_shared: false
});

// ==============================================================================
// UC2 Node Type 4: PhysicsConstraint (10 samples)
// ==============================================================================

// Sample 1: Temperature Constraint - Railway PLC
CREATE (constraint1:PhysicsConstraint {
  constraintId: "constraint-plc001-temperature",
  assetId: "device-plc-rail-001",
  parameter: "temperature",
  minValue: 60.0,
  maxValue: 95.0,
  unit: "°C",
  consequence: "SAFETY_HAZARD",
  severity: "CRITICAL",
  physicsLaw: "Thermodynamics First Law - Exceeding max temp causes thermal runaway",
  violationAction: "ENGAGE_SAFETY",
  customer_namespace: "shared:physics",
  is_shared: true
});

// Sample 2: Rotation Speed Constraint - Centrifuge
CREATE (constraint2:PhysicsConstraint {
  constraintId: "constraint-centrifuge001-speed",
  assetId: "device-centrifuge-001",
  parameter: "rotationSpeed",
  minValue: 900.0,
  maxValue: 1200.0,
  unit: "RPM",
  consequence: "MECHANICAL_FAILURE",
  severity: "CRITICAL",
  physicsLaw: "Exceeding max RPM causes rotor stress and potential catastrophic failure",
  violationAction: "SHUTDOWN",
  customer_namespace: "shared:physics",
  is_shared: true
});

// Sample 3: Pressure Constraint - Water Pump
CREATE (constraint3:PhysicsConstraint {
  constraintId: "constraint-pump001-pressure",
  assetId: "device-pump-water-001",
  parameter: "pressure",
  minValue: 60.0,
  maxValue: 120.0,
  unit: "PSI",
  consequence: "DAMAGE",
  severity: "HIGH",
  physicsLaw: "Bernoulli's Principle - Excessive pressure causes pipe rupture",
  violationAction: "REDUCE_LOAD",
  customer_namespace: "shared:physics",
  is_shared: true
});

// Sample 4: Voltage Constraint - Transformer
CREATE (constraint4:PhysicsConstraint {
  constraintId: "constraint-transformer001-voltage",
  assetId: "device-transformer-001",
  parameter: "voltage",
  minValue: 125000.0,
  maxValue: 145000.0,
  unit: "V",
  consequence: "REGULATORY_VIOLATION",
  severity: "CRITICAL",
  physicsLaw: "Ohm's Law - Voltage exceeding design limits causes insulation breakdown",
  violationAction: "SHUTDOWN",
  customer_namespace: "shared:physics",
  is_shared: true
});

// Sample 5: Temperature Constraint - Industrial Furnace
CREATE (constraint5:PhysicsConstraint {
  constraintId: "constraint-furnace001-temperature",
  assetId: "device-furnace-001",
  parameter: "temperature",
  minValue: 1000.0,
  maxValue: 1350.0,
  unit: "°C",
  consequence: "DAMAGE",
  severity: "HIGH",
  physicsLaw: "Thermal expansion limits - Exceeding max temp causes structural failure",
  violationAction: "ALARM",
  customer_namespace: "shared:physics",
  is_shared: true
});

// Sample 6: Humidity Constraint - HVAC
CREATE (constraint6:PhysicsConstraint {
  constraintId: "constraint-hvac001-humidity",
  assetId: "device-hvac-001",
  parameter: "humidity",
  minValue: 30.0,
  maxValue: 60.0,
  unit: "%",
  consequence: "PERFORMANCE_DEGRADATION",
  severity: "MEDIUM",
  physicsLaw: "Psychrometrics - Humidity outside range causes comfort issues",
  violationAction: "NOTIFY",
  customer_namespace: "shared:physics",
  is_shared: true
});

// Sample 7: Vibration Constraint - Gas Compressor
CREATE (constraint7:PhysicsConstraint {
  constraintId: "constraint-compressor001-vibration",
  assetId: "device-compressor-001",
  parameter: "vibration",
  minValue: 0.0,
  maxValue: 5.0,
  unit: "Hz",
  consequence: "FAILURE",
  severity: "HIGH",
  physicsLaw: "Resonance frequency - Excessive vibration causes bearing failure",
  violationAction: "SHUTDOWN",
  customer_namespace: "shared:physics",
  is_shared: true
});

// Sample 8: Current Constraint - Signal Controller
CREATE (constraint8:PhysicsConstraint {
  constraintId: "constraint-signal001-current",
  assetId: "device-signal-controller-001",
  parameter: "current",
  minValue: 0.5,
  maxValue: 1.2,
  unit: "A",
  consequence: "SAFETY_HAZARD",
  severity: "CRITICAL",
  physicsLaw: "Electrical safety - Current out of range indicates fault",
  violationAction: "ENGAGE_SAFETY",
  customer_namespace: "shared:physics",
  is_shared: true
});

// Sample 9: Pressure Constraint - Chemical Reactor
CREATE (constraint9:PhysicsConstraint {
  constraintId: "constraint-reactor001-pressure",
  assetId: "device-reactor-001",
  parameter: "pressure",
  minValue: 8.0,
  maxValue: 15.0,
  unit: "bar",
  consequence: "SAFETY_HAZARD",
  severity: "CRITICAL",
  physicsLaw: "Conservation of Mass - Pressure buildup indicates runaway reaction",
  violationAction: "ENGAGE_SAFETY",
  customer_namespace: "shared:physics",
  is_shared: true
});

// Sample 10: Wind Speed Constraint - Wind Turbine
CREATE (constraint10:PhysicsConstraint {
  constraintId: "constraint-turbine001-windspeed",
  assetId: "device-turbine-001",
  parameter: "windSpeed",
  minValue: 3.0,
  maxValue: 25.0,
  unit: "m/s",
  consequence: "DAMAGE",
  severity: "HIGH",
  physicsLaw: "Structural limits - Wind speed beyond cutout speed causes damage",
  violationAction: "SHUTDOWN",
  customer_namespace: "shared:physics",
  is_shared: true
});

// ==============================================================================
// UC2 Node Type 5: SafetyFunction (10 samples)
// ==============================================================================

// Sample 1: Emergency Stop - Railway PLC
CREATE (safety1:SafetyFunction {
  functionId: "safety-func-emergency-stop-01",
  functionName: "Emergency Stop",
  silLevel: "SIL_3",
  logicDescription: "IF (temp > 95 OR pressure > 150) AND NOT bypass_active THEN shutdown",
  inputs: ["sensor-temp-plc001-01", "sensor-pressure-plc001-01", "bypass-switch-01"],
  outputs: ["actuator-valve-plc001-01", "actuator-alarm-01"],
  failSafeState: "SHUTDOWN",
  standard: "IEC_61508",
  certificateNumber: "TUV-SIL3-2023-001234",
  testFrequency: duration('PT720H'),
  lastTestDate: datetime('2025-10-15T10:00:00Z'),
  nextTestDue: datetime('2025-11-14T10:00:00Z'),
  assetId: "device-plc-rail-001",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Overspeed Protection - Centrifuge
CREATE (safety2:SafetyFunction {
  functionId: "safety-func-overspeed-01",
  functionName: "Overspeed Protection",
  silLevel: "SIL_4",
  logicDescription: "IF rotationSpeed > 1200 THEN emergency_brake",
  inputs: ["sensor-speed-centrifuge001-01"],
  outputs: ["actuator-motor-centrifuge001-01", "brake-system-01"],
  failSafeState: "BRAKE_ENGAGED",
  standard: "IEC_61508",
  certificateNumber: "TUV-SIL4-2024-005678",
  testFrequency: duration('PT168H'),
  lastTestDate: datetime('2025-11-06T14:00:00Z'),
  nextTestDue: datetime('2025-11-13T14:00:00Z'),
  assetId: "device-centrifuge-001",
  customer_namespace: "customer:NuclearFacility-Alpha",
  is_shared: false
});

// Sample 3: High Pressure Shutdown - Water Pump
CREATE (safety3:SafetyFunction {
  functionId: "safety-func-high-pressure-01",
  functionName: "High Pressure Shutdown",
  silLevel: "SIL_2",
  logicDescription: "IF pressure > 120 THEN stop_pump",
  inputs: ["sensor-pressure-pump001-01"],
  outputs: ["actuator-pump-water001-01", "alarm-panel-01"],
  failSafeState: "PUMP_STOPPED",
  standard: "IEC_61511",
  certificateNumber: "TUV-SIL2-2023-009876",
  testFrequency: duration('PT1440H'),
  lastTestDate: datetime('2025-09-20T08:00:00Z'),
  nextTestDue: datetime('2025-11-29T08:00:00Z'),
  assetId: "device-pump-water-001",
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 4: Overvoltage Protection - Transformer
CREATE (safety4:SafetyFunction {
  functionId: "safety-func-overvoltage-01",
  functionName: "Overvoltage Protection",
  silLevel: "SIL_3",
  logicDescription: "IF voltage > 145000 THEN trip_breaker",
  inputs: ["sensor-voltage-transformer001-01"],
  outputs: ["actuator-breaker-transformer001-01"],
  failSafeState: "BREAKER_OPEN",
  standard: "IEC_61508",
  certificateNumber: "TUV-SIL3-2024-003456",
  testFrequency: duration('PT720H'),
  lastTestDate: datetime('2025-10-01T12:00:00Z'),
  nextTestDue: datetime('2025-11-01T12:00:00Z'),
  assetId: "device-transformer-001",
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// Sample 5: Overtemperature Shutdown - Furnace
CREATE (safety5:SafetyFunction {
  functionId: "safety-func-overtemp-furnace-01",
  functionName: "Overtemperature Shutdown",
  silLevel: "SIL_2",
  logicDescription: "IF temperature > 1350 THEN shutoff_fuel",
  inputs: ["sensor-temp-furnace001-01"],
  outputs: ["actuator-heater-furnace001-01", "fuel-valve-01"],
  failSafeState: "FUEL_CLOSED",
  standard: "IEC_61511",
  certificateNumber: "TUV-SIL2-2023-007890",
  testFrequency: duration('PT1440H'),
  lastTestDate: datetime('2025-08-15T09:00:00Z'),
  nextTestDue: datetime('2025-10-24T09:00:00Z'),
  assetId: "device-furnace-001",
  customer_namespace: "customer:SteelMill-Delta",
  is_shared: false
});

// Sample 6: Fire Suppression - HVAC
CREATE (safety6:SafetyFunction {
  functionId: "safety-func-fire-suppression-01",
  functionName: "Fire Suppression Activation",
  silLevel: "SIL_3",
  logicDescription: "IF smoke_detected OR temp > 100 THEN activate_suppression",
  inputs: ["sensor-smoke-hvac001-01", "sensor-temp-hvac001-01"],
  outputs: ["fire-suppression-system-01", "alarm-system-01"],
  failSafeState: "SYSTEM_ACTIVATED",
  standard: "EN_50128",
  certificateNumber: "TUV-SIL3-2024-002345",
  testFrequency: duration('PT720H'),
  lastTestDate: datetime('2025-10-10T11:00:00Z'),
  nextTestDue: datetime('2025-11-09T11:00:00Z'),
  assetId: "device-hvac-001",
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 7: Vibration Shutdown - Gas Compressor
CREATE (safety7:SafetyFunction {
  functionId: "safety-func-vibration-shutdown-01",
  functionName: "High Vibration Shutdown",
  silLevel: "SIL_2",
  logicDescription: "IF vibration > 5.0 THEN stop_compressor",
  inputs: ["sensor-vibration-compressor001-01"],
  outputs: ["actuator-motor-compressor001-01"],
  failSafeState: "COMPRESSOR_STOPPED",
  standard: "IEC_61511",
  certificateNumber: "TUV-SIL2-2023-004567",
  testFrequency: duration('PT1440H'),
  lastTestDate: datetime('2025-09-01T10:00:00Z'),
  nextTestDue: datetime('2025-11-10T10:00:00Z'),
  assetId: "device-compressor-001",
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// Sample 8: Signal Fault Detection - Railway Signal
CREATE (safety8:SafetyFunction {
  functionId: "safety-func-signal-fault-01",
  functionName: "Signal Fault Detection",
  silLevel: "SIL_4",
  logicDescription: "IF current < 0.5 OR voltage < 20 THEN signal_to_red",
  inputs: ["sensor-current-signal001-01", "sensor-voltage-signal001-01"],
  outputs: ["actuator-relay-signal001-01"],
  failSafeState: "SIGNAL_RED",
  standard: "EN_50128",
  certificateNumber: "TUV-SIL4-2024-008901",
  testFrequency: duration('PT168H'),
  lastTestDate: datetime('2025-11-06T08:00:00Z'),
  nextTestDue: datetime('2025-11-13T08:00:00Z'),
  assetId: "device-signal-controller-001",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 9: Pressure Relief - Chemical Reactor
CREATE (safety9:SafetyFunction {
  functionId: "safety-func-pressure-relief-01",
  functionName: "Emergency Pressure Relief",
  silLevel: "SIL_3",
  logicDescription: "IF pressure > 15 OR temp > 200 THEN open_relief_valve",
  inputs: ["sensor-pressure-reactor001-01", "sensor-temp-reactor001-01"],
  outputs: ["relief-valve-01", "cooling-system-01"],
  failSafeState: "VALVE_OPEN",
  standard: "IEC_61511",
  certificateNumber: "TUV-SIL3-2023-006789",
  testFrequency: duration('PT720H'),
  lastTestDate: datetime('2025-10-05T13:00:00Z'),
  nextTestDue: datetime('2025-11-04T13:00:00Z'),
  assetId: "device-reactor-001",
  customer_namespace: "customer:ChemPlant-Eta",
  is_shared: false
});

// Sample 10: Overspeed Shutdown - Wind Turbine
CREATE (safety10:SafetyFunction {
  functionId: "safety-func-overspeed-turbine-01",
  functionName: "Wind Turbine Overspeed Protection",
  silLevel: "SIL_2",
  logicDescription: "IF windSpeed > 25 OR rotorSpeed > 15 THEN feather_blades",
  inputs: ["sensor-windspeed-turbine001-01", "sensor-rotorspeed-turbine001-01"],
  outputs: ["actuator-motor-turbine001-01", "brake-system-turbine001-01"],
  failSafeState: "BLADES_FEATHERED",
  standard: "IEC_61508",
  certificateNumber: "TUV-SIL2-2024-001234",
  testFrequency: duration('PT1440H'),
  lastTestDate: datetime('2025-09-10T14:00:00Z'),
  nextTestDue: datetime('2025-11-19T14:00:00Z'),
  assetId: "device-turbine-001",
  customer_namespace: "customer:WindFarm-Theta",
  is_shared: false
});

// ==============================================================================
// END OF UC2 SAMPLE DATA
// ==============================================================================
// Total UC2 Nodes Created: 50 nodes (10 per type × 5 types)
// Coverage: DigitalTwinState, PhysicalSensor, PhysicalActuator,
//           PhysicsConstraint, SafetyFunction
// Realistic data includes normal operations, anomalies, failures, and edge cases
// ==============================================================================
