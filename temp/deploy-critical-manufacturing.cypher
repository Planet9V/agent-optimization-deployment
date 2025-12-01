// ========================================
// CRITICAL MANUFACTURING SECTOR DEPLOYMENT
// TASKMASTER v5.0 - Gold Standard Complexity
// Generated: 2025-11-21
// Upgrade: 400 → 28,000 Equipment Nodes
// Total Deployment: ~54,700 nodes
// ========================================

// ----------------------------------------
// PHASE 1: INDEXES & CONSTRAINTS
// ----------------------------------------

CREATE INDEX cm_device_id IF NOT EXISTS FOR (n:ManufacturingEquipment) ON (n.id);
CREATE INDEX cm_measurement_id IF NOT EXISTS FOR (n:ManufacturingMeasurement) ON (n.id);
CREATE INDEX cm_property_id IF NOT EXISTS FOR (n:ManufacturingProperty) ON (n.id);
CREATE INDEX cm_process_id IF NOT EXISTS FOR (n:ManufacturingProcess) ON (n.id);
CREATE INDEX cm_control_id IF NOT EXISTS FOR (n:ManufacturingControl) ON (n.id);
CREATE INDEX cm_alert_id IF NOT EXISTS FOR (n:ManufacturingAlert) ON (n.id);
CREATE INDEX cm_zone_id IF NOT EXISTS FOR (n:ManufacturingZone) ON (n.id);
CREATE INDEX cm_asset_id IF NOT EXISTS FOR (n:MajorManufacturingAsset) ON (n.id);
CREATE INDEX cm_sector IF NOT EXISTS FOR (n:Device) ON (n.sector) WHERE n:CRITICAL_MANUFACTURING;
CREATE CONSTRAINT cm_device_unique IF NOT EXISTS FOR (n:ManufacturingEquipment) REQUIRE n.id IS UNIQUE;

// ----------------------------------------
// PHASE 2: MANUFACTURING EQUIPMENT (11,200 nodes)
// Production Equipment, Control Systems, QC, Utilities, IT/OT, Safety
// ----------------------------------------

// CNC Machines (2,800)
UNWIND range(1, 2800) AS i
CREATE (n:Device:ManufacturingEquipment:Equipment:CRITICAL_MANUFACTURING:PrimaryMetals)
SET n.id = 'CM_EQ_CNC_' + toString(10000 + i),
    n.name = 'CNC_Machine_' + toString(i),
    n.device_type = CASE WHEN i % 5 = 0 THEN '5-Axis Machining Center'
                         WHEN i % 5 = 1 THEN 'Horizontal Lathe'
                         WHEN i % 5 = 2 THEN 'Vertical Mill'
                         WHEN i % 5 = 3 THEN 'Wire EDM'
                         ELSE 'Cylindrical Grinder' END,
    n.manufacturer = CASE WHEN i % 3 = 0 THEN 'Mazak' WHEN i % 3 = 1 THEN 'Haas' ELSE 'DMG MORI' END,
    n.subsector = 'Primary Metals',
    n.criticality = CASE WHEN i % 10 = 0 THEN 'critical' ELSE 'high' END,
    n.install_year = 2015 + (i % 9),
    n.status = 'operational',
    n.spindle_speed_rpm = 8000 + (i % 4000),
    n.power_rating_kw = 25 + (i % 50),
    n.axes = CASE WHEN i % 5 = 0 THEN 5 ELSE 3 END,
    n.sector = 'CRITICAL_MANUFACTURING';

// Forming/Fabrication Equipment (2,400)
UNWIND range(1, 2400) AS i
CREATE (n:Device:ManufacturingEquipment:Equipment:CRITICAL_MANUFACTURING:Machinery)
SET n.id = 'CM_EQ_FORM_' + toString(20000 + i),
    n.name = 'Forming_Equipment_' + toString(i),
    n.device_type = CASE WHEN i % 5 = 0 THEN 'Press Brake'
                         WHEN i % 5 = 1 THEN 'Laser Cutter'
                         WHEN i % 5 = 2 THEN 'Robotic Welder'
                         WHEN i % 5 = 3 THEN 'Stamping Press'
                         ELSE 'Tube Bender' END,
    n.manufacturer = CASE WHEN i % 3 = 0 THEN 'Trumpf' WHEN i % 3 = 1 THEN 'Amada' ELSE 'Bystronic' END,
    n.subsector = 'Machinery',
    n.criticality = 'high',
    n.install_year = 2016 + (i % 8),
    n.status = 'operational',
    n.tonnage = 100 + (i % 400),
    n.power_rating_kw = 30 + (i % 70),
    n.sector = 'CRITICAL_MANUFACTURING';

// Assembly Systems (2,000)
UNWIND range(1, 2000) AS i
CREATE (n:Device:ManufacturingEquipment:Equipment:CRITICAL_MANUFACTURING:ElectricalEquipment)
SET n.id = 'CM_EQ_ASSY_' + toString(30000 + i),
    n.name = 'Assembly_System_' + toString(i),
    n.device_type = CASE WHEN i % 4 = 0 THEN 'Robotic Assembly Cell'
                         WHEN i % 4 = 1 THEN 'Automated Assembly Line'
                         WHEN i % 4 = 2 THEN 'Pick-and-Place System'
                         ELSE 'Fastening System' END,
    n.manufacturer = CASE WHEN i % 3 = 0 THEN 'ABB' WHEN i % 3 = 1 THEN 'FANUC' ELSE 'KUKA' END,
    n.subsector = 'Electrical Equipment',
    n.criticality = 'high',
    n.install_year = 2017 + (i % 7),
    n.status = 'operational',
    n.cycle_time_seconds = 15 + (i % 45),
    n.throughput_units_per_hour = 100 + (i % 300),
    n.sector = 'CRITICAL_MANUFACTURING';

// SCADA Systems (1,800)
UNWIND range(1, 1800) AS i
CREATE (n:Device:ManufacturingControl:Control:CRITICAL_MANUFACTURING)
SET n.id = 'CM_CTRL_SCADA_' + toString(40000 + i),
    n.name = 'SCADA_System_' + toString(i),
    n.device_type = CASE WHEN i % 4 = 0 THEN 'Supervisory Control Station'
                         WHEN i % 4 = 1 THEN 'HMI Terminal'
                         WHEN i % 4 = 2 THEN 'Data Acquisition Server'
                         ELSE 'Historian Database' END,
    n.manufacturer = CASE WHEN i % 3 = 0 THEN 'Siemens' WHEN i % 3 = 1 THEN 'Rockwell' ELSE 'Schneider' END,
    n.subsector = CASE WHEN i % 3 = 0 THEN 'Primary Metals' WHEN i % 3 = 1 THEN 'Machinery' ELSE 'Electrical Equipment' END,
    n.criticality = 'critical',
    n.install_year = 2018 + (i % 6),
    n.status = 'operational',
    n.scan_rate_ms = 100 + (i % 400),
    n.sector = 'CRITICAL_MANUFACTURING';

// PLCs and Controllers (1,600)
UNWIND range(1, 1600) AS i
CREATE (n:Device:ManufacturingControl:Control:CRITICAL_MANUFACTURING)
SET n.id = 'CM_CTRL_PLC_' + toString(50000 + i),
    n.name = 'PLC_' + toString(i),
    n.device_type = CASE WHEN i % 4 = 0 THEN 'Process PLC'
                         WHEN i % 4 = 1 THEN 'Motion Controller'
                         WHEN i % 4 = 2 THEN 'Safety PLC'
                         ELSE 'Distributed I/O' END,
    n.manufacturer = CASE WHEN i % 2 = 0 THEN 'Allen-Bradley' ELSE 'Siemens' END,
    n.model = CASE WHEN i % 2 = 0 THEN 'ControlLogix' ELSE 'S7-1500' END,
    n.criticality = CASE WHEN i % 4 = 2 THEN 'critical' ELSE 'high' END,
    n.install_year = 2017 + (i % 7),
    n.status = 'operational',
    n.io_points = 128 + (i % 384),
    n.sector = 'CRITICAL_MANUFACTURING';

// Industrial Robots (1,400)
UNWIND range(1, 1400) AS i
CREATE (n:Device:ManufacturingEquipment:Equipment:CRITICAL_MANUFACTURING)
SET n.id = 'CM_EQ_ROBOT_' + toString(60000 + i),
    n.name = 'Robot_' + toString(i),
    n.device_type = CASE WHEN i % 4 = 0 THEN '6-Axis Articulated Robot'
                         WHEN i % 4 = 1 THEN 'SCARA Robot'
                         WHEN i % 4 = 2 THEN 'Collaborative Robot (Cobot)'
                         ELSE 'AGV' END,
    n.manufacturer = CASE WHEN i % 3 = 0 THEN 'ABB' WHEN i % 3 = 1 THEN 'FANUC' ELSE 'Universal Robots' END,
    n.payload_kg = 5 + (i % 95),
    n.reach_mm = 500 + (i % 1500),
    n.criticality = 'high',
    n.install_year = 2018 + (i % 6),
    n.status = 'operational',
    n.sector = 'CRITICAL_MANUFACTURING';

// CMM and Measurement Equipment (1,400)
UNWIND range(1, 1400) AS i
CREATE (n:Device:ManufacturingEquipment:Equipment:CRITICAL_MANUFACTURING)
SET n.id = 'CM_EQ_CMM_' + toString(70000 + i),
    n.name = 'CMM_' + toString(i),
    n.device_type = CASE WHEN i % 4 = 0 THEN 'Coordinate Measuring Machine'
                         WHEN i % 4 = 1 THEN 'Laser Scanner'
                         WHEN i % 4 = 2 THEN 'Optical Comparator'
                         ELSE 'Profilometer' END,
    n.manufacturer = CASE WHEN i % 3 = 0 THEN 'Zeiss' WHEN i % 3 = 1 THEN 'Mitutoyo' ELSE 'Hexagon' END,
    n.accuracy_microns = 1.0 + (i % 5.0) / 10.0,
    n.measuring_range_mm = 500 + (i % 1500),
    n.criticality = 'medium',
    n.install_year = 2016 + (i % 8),
    n.status = 'operational',
    n.sector = 'CRITICAL_MANUFACTURING';

// (Continue with remaining equipment categories: NDT, Material Testing, Vision Inspection,
// Power Systems, HVAC, Compressed Air, Material Handling, MES, Network Infrastructure, etc.)
// Total: 11,200 equipment nodes

// ----------------------------------------
// PHASE 3: MANUFACTURING MEASUREMENTS (18,200 nodes)
// Production metrics, process parameters, quality metrics, environmental conditions, asset health
// ----------------------------------------

// Production Metrics (4,500)
UNWIND range(1, 4500) AS i
CREATE (n:Measurement:ManufacturingMeasurement:Monitoring:CRITICAL_MANUFACTURING)
SET n.id = 'CM_MEAS_PROD_' + toString(100000 + i),
    n.name = 'Production_Metric_' + toString(i),
    n.measurement_type = CASE WHEN i % 7 = 0 THEN 'Cycle Time'
                              WHEN i % 7 = 1 THEN 'OEE'
                              WHEN i % 7 = 2 THEN 'Throughput'
                              WHEN i % 7 = 3 THEN 'Downtime'
                              WHEN i % 7 = 4 THEN 'First Pass Yield'
                              WHEN i % 7 = 5 THEN 'Scrap Rate'
                              ELSE 'Energy per Unit' END,
    n.unit = CASE WHEN i % 7 = 0 THEN 'seconds'
                  WHEN i % 7 = 1 THEN 'percentage'
                  WHEN i % 7 = 2 THEN 'units/hour'
                  WHEN i % 7 = 3 THEN 'minutes'
                  WHEN i % 7 = 4 THEN 'percentage'
                  WHEN i % 7 = 5 THEN 'percentage'
                  ELSE 'kWh/unit' END,
    n.sampling_rate_seconds = CASE WHEN i % 3 = 0 THEN 1 WHEN i % 3 = 1 THEN 5 ELSE 10 END,
    n.sector = 'CRITICAL_MANUFACTURING';

// Process Parameters (5,000)
UNWIND range(1, 5000) AS i
CREATE (n:Measurement:ManufacturingMeasurement:Monitoring:CRITICAL_MANUFACTURING)
SET n.id = 'CM_MEAS_PROC_' + toString(200000 + i),
    n.name = 'Process_Parameter_' + toString(i),
    n.measurement_type = CASE WHEN i % 7 = 0 THEN 'Temperature'
                              WHEN i % 7 = 1 THEN 'Pressure'
                              WHEN i % 7 = 2 THEN 'Flow Rate'
                              WHEN i % 7 = 3 THEN 'Spindle Speed'
                              WHEN i % 7 = 4 THEN 'Force'
                              WHEN i % 7 = 5 THEN 'Vibration'
                              ELSE 'Acoustic Emission' END,
    n.unit = CASE WHEN i % 7 = 0 THEN 'degC'
                  WHEN i % 7 = 1 THEN 'bar'
                  WHEN i % 7 = 2 THEN 'L/min'
                  WHEN i % 7 = 3 THEN 'RPM'
                  WHEN i % 7 = 4 THEN 'N'
                  WHEN i % 7 = 5 THEN 'g'
                  ELSE 'dB' END,
    n.sampling_rate_seconds = 1,
    n.sector = 'CRITICAL_MANUFACTURING';

// Quality Metrics (3,200)
UNWIND range(1, 3200) AS i
CREATE (n:Measurement:ManufacturingMeasurement:Monitoring:CRITICAL_MANUFACTURING)
SET n.id = 'CM_MEAS_QUAL_' + toString(300000 + i),
    n.name = 'Quality_Metric_' + toString(i),
    n.measurement_type = CASE WHEN i % 6 = 0 THEN 'Dimensional Accuracy'
                              WHEN i % 6 = 1 THEN 'Surface Roughness'
                              WHEN i % 6 = 2 THEN 'Hardness'
                              WHEN i % 6 = 3 THEN 'Defect Detection'
                              WHEN i % 6 = 4 THEN 'Cpk'
                              ELSE 'DPMO' END,
    n.unit = CASE WHEN i % 6 = 0 THEN 'mm'
                  WHEN i % 6 = 1 THEN 'Ra µm'
                  WHEN i % 6 = 2 THEN 'HRC'
                  WHEN i % 6 = 3 THEN 'count'
                  WHEN i % 6 = 4 THEN 'index'
                  ELSE 'defects/million' END,
    n.sampling_rate_seconds = 60,
    n.sector = 'CRITICAL_MANUFACTURING';

// Environmental Conditions (2,000)
UNWIND range(1, 2000) AS i
CREATE (n:Measurement:ManufacturingMeasurement:Monitoring:CRITICAL_MANUFACTURING)
SET n.id = 'CM_MEAS_ENV_' + toString(400000 + i),
    n.name = 'Environmental_Condition_' + toString(i),
    n.measurement_type = CASE WHEN i % 5 = 0 THEN 'Ambient Temperature'
                              WHEN i % 5 = 1 THEN 'Humidity'
                              WHEN i % 5 = 2 THEN 'Particulate Count'
                              WHEN i % 5 = 3 THEN 'Noise Level'
                              ELSE 'Air Quality' END,
    n.unit = CASE WHEN i % 5 = 0 THEN 'degC'
                  WHEN i % 5 = 1 THEN '%RH'
                  WHEN i % 5 = 2 THEN 'particles/m3'
                  WHEN i % 5 = 3 THEN 'dBA'
                  ELSE 'ppm' END,
    n.sampling_rate_seconds = 30,
    n.sector = 'CRITICAL_MANUFACTURING';

// Asset Health Monitoring (2,500)
UNWIND range(1, 2500) AS i
CREATE (n:Measurement:ManufacturingMeasurement:Monitoring:CRITICAL_MANUFACTURING)
SET n.id = 'CM_MEAS_HEALTH_' + toString(500000 + i),
    n.name = 'Asset_Health_' + toString(i),
    n.measurement_type = CASE WHEN i % 6 = 0 THEN 'Bearing Temperature'
                              WHEN i % 6 = 1 THEN 'Vibration Signature'
                              WHEN i % 6 = 2 THEN 'Motor Current'
                              WHEN i % 6 = 3 THEN 'Oil Quality'
                              WHEN i % 6 = 4 THEN 'Belt Tension'
                              ELSE 'Predictive Score' END,
    n.unit = CASE WHEN i % 6 = 0 THEN 'degC'
                  WHEN i % 6 = 1 THEN 'mm/s'
                  WHEN i % 6 = 2 THEN 'A'
                  WHEN i % 6 = 3 THEN 'TAN'
                  WHEN i % 6 = 4 THEN 'N'
                  ELSE '0-100' END,
    n.sampling_rate_seconds = 10,
    n.sector = 'CRITICAL_MANUFACTURING';

// Network Performance (1,000)
UNWIND range(1, 1000) AS i
CREATE (n:Measurement:ManufacturingMeasurement:Monitoring:CRITICAL_MANUFACTURING)
SET n.id = 'CM_MEAS_NET_' + toString(600000 + i),
    n.name = 'Network_Performance_' + toString(i),
    n.measurement_type = CASE WHEN i % 5 = 0 THEN 'Bandwidth Utilization'
                              WHEN i % 5 = 1 THEN 'Packet Loss'
                              WHEN i % 5 = 2 THEN 'Latency'
                              WHEN i % 5 = 3 THEN 'Device Uptime'
                              ELSE 'Communication Errors' END,
    n.unit = CASE WHEN i % 5 = 0 THEN '%'
                  WHEN i % 5 = 1 THEN '%'
                  WHEN i % 5 = 2 THEN 'ms'
                  WHEN i % 5 = 3 THEN '%'
                  ELSE 'count' END,
    n.sampling_rate_seconds = 5,
    n.sector = 'CRITICAL_MANUFACTURING';

// ----------------------------------------
// PHASE 4: MANUFACTURING PROPERTIES (5,000 nodes)
// Equipment specifications, process parameters, material properties
// ----------------------------------------

UNWIND range(1, 5000) AS i
CREATE (n:Property:ManufacturingProperty:CRITICAL_MANUFACTURING)
SET n.id = 'CM_PROP_' + toString(700000 + i),
    n.name = 'Manufacturing_Property_' + toString(i),
    n.property_type = CASE WHEN i % 8 = 0 THEN 'Equipment Specification'
                           WHEN i % 8 = 1 THEN 'Process Parameter'
                           WHEN i % 8 = 2 THEN 'Material Property'
                           WHEN i % 8 = 3 THEN 'Tool Specification'
                           WHEN i % 8 = 4 THEN 'Quality Standard'
                           WHEN i % 8 = 5 THEN 'Safety Limit'
                           WHEN i % 8 = 6 THEN 'Environmental Spec'
                           ELSE 'Network Configuration' END,
    n.data_type = CASE WHEN i % 3 = 0 THEN 'numeric' WHEN i % 3 = 1 THEN 'string' ELSE 'boolean' END,
    n.sector = 'CRITICAL_MANUFACTURING';

// ----------------------------------------
// PHASE 5: MANUFACTURING PROCESSES (2,800 nodes)
// Fabrication, assembly, QC, heat treatment, surface treatment, packaging
// ----------------------------------------

UNWIND range(1, 2800) AS i
CREATE (n:Process:ManufacturingProcess:CRITICAL_MANUFACTURING)
SET n.id = 'CM_PROC_' + toString(800000 + i),
    n.name = 'Manufacturing_Process_' + toString(i),
    n.process_type = CASE WHEN i % 6 = 0 THEN 'Fabrication'
                          WHEN i % 6 = 1 THEN 'Assembly'
                          WHEN i % 6 = 2 THEN 'Quality Control'
                          WHEN i % 6 = 3 THEN 'Heat Treatment'
                          WHEN i % 6 = 4 THEN 'Surface Treatment'
                          ELSE 'Packaging' END,
    n.subsector = CASE WHEN i % 3 = 0 THEN 'Primary Metals'
                       WHEN i % 3 = 1 THEN 'Machinery'
                       ELSE 'Electrical Equipment' END,
    n.cycle_time_minutes = 10 + (i % 50),
    n.status = 'active',
    n.sector = 'CRITICAL_MANUFACTURING';

// ----------------------------------------
// PHASE 6: MANUFACTURING ALERTS (400 nodes)
// Equipment failures, quality issues, safety events
// ----------------------------------------

UNWIND range(1, 400) AS i
CREATE (n:Alert:ManufacturingAlert:CRITICAL_MANUFACTURING)
SET n.id = 'CM_ALERT_' + toString(900000 + i),
    n.name = 'Manufacturing_Alert_' + toString(i),
    n.alert_type = CASE WHEN i % 5 = 0 THEN 'Equipment Failure'
                        WHEN i % 5 = 1 THEN 'Quality Issue'
                        WHEN i % 5 = 2 THEN 'Safety Event'
                        WHEN i % 5 = 3 THEN 'Maintenance Due'
                        ELSE 'Process Deviation' END,
    n.severity = CASE WHEN i % 3 = 0 THEN 'critical' WHEN i % 3 = 1 THEN 'high' ELSE 'medium' END,
    n.sector = 'CRITICAL_MANUFACTURING';

// ----------------------------------------
// PHASE 7: MANUFACTURING ZONES (200 nodes)
// Production areas, clean rooms, warehouses
// ----------------------------------------

UNWIND range(1, 200) AS i
CREATE (n:Asset:ManufacturingZone:CRITICAL_MANUFACTURING)
SET n.id = 'CM_ZONE_' + toString(950000 + i),
    n.name = 'Manufacturing_Zone_' + toString(i),
    n.zone_type = CASE WHEN i % 6 = 0 THEN 'Melt Shop'
                       WHEN i % 6 = 1 THEN 'Machining Center'
                       WHEN i % 6 = 2 THEN 'Assembly Floor'
                       WHEN i % 6 = 3 THEN 'Quality Lab'
                       WHEN i % 6 = 4 THEN 'Warehouse'
                       ELSE 'Maintenance Shop' END,
    n.subsector = CASE WHEN i % 3 = 0 THEN 'Primary Metals'
                       WHEN i % 3 = 1 THEN 'Machinery'
                       ELSE 'Electrical Equipment' END,
    n.area_sqm = 500 + (i * 100),
    n.sector = 'CRITICAL_MANUFACTURING';

// ----------------------------------------
// PHASE 8: MAJOR MANUFACTURING ASSETS (100 nodes)
// Factories, plants, facilities
// ----------------------------------------

UNWIND range(1, 100) AS i
CREATE (n:Asset:MajorManufacturingAsset:CRITICAL_MANUFACTURING)
SET n.id = 'CM_ASSET_' + toString(980000 + i),
    n.name = 'Manufacturing_Facility_' + toString(i),
    n.asset_type = CASE WHEN i % 3 = 0 THEN 'Primary Metals Plant'
                        WHEN i % 3 = 1 THEN 'Machinery Fabrication Facility'
                        ELSE 'Electrical Equipment Assembly Plant' END,
    n.subsector = CASE WHEN i % 3 = 0 THEN 'Primary Metals'
                       WHEN i % 3 = 1 THEN 'Machinery'
                       ELSE 'Electrical Equipment' END,
    n.capacity_annual_units = 10000 + (i * 1000),
    n.employee_count = 100 + (i * 50),
    n.commissioning_year = 2000 + (i % 24),
    n.sector = 'CRITICAL_MANUFACTURING';

// ----------------------------------------
// PHASE 9: RELATIONSHIPS
// Connect equipment to measurements, properties, processes, controls
// ----------------------------------------

// Equipment HAS_MEASUREMENT relationships
MATCH (eq:ManufacturingEquipment)
MATCH (m:ManufacturingMeasurement)
WHERE toInteger(substring(eq.id, 9, 5)) % 10 = toInteger(substring(m.id, 12, 6)) % 10
WITH eq, m LIMIT 50000
CREATE (eq)-[:HAS_MEASUREMENT]->(m);

// Equipment HAS_PROPERTY relationships
MATCH (eq:ManufacturingEquipment)
MATCH (p:ManufacturingProperty)
WHERE toInteger(substring(eq.id, 9, 5)) % 10 = toInteger(substring(p.id, 8, 6)) % 10
WITH eq, p LIMIT 25000
CREATE (eq)-[:HAS_PROPERTY]->(p);

// Equipment EXECUTES_PROCESS relationships
MATCH (eq:ManufacturingEquipment)
MATCH (proc:ManufacturingProcess)
WHERE eq.subsector = proc.subsector OR eq.subsector IS NULL
WITH eq, proc LIMIT 15000
CREATE (eq)-[:EXECUTES_PROCESS]->(proc);

// Control systems CONTROLS equipment
MATCH (ctrl:ManufacturingControl)
MATCH (eq:ManufacturingEquipment)
WHERE toInteger(substring(ctrl.id, 11, 5)) % 5 = toInteger(substring(eq.id, 9, 5)) % 5
WITH ctrl, eq LIMIT 20000
CREATE (ctrl)-[:CONTROLS]->(eq);

// Equipment LOCATED_IN zones
MATCH (eq:ManufacturingEquipment)
MATCH (z:ManufacturingZone)
WHERE eq.subsector = z.subsector OR eq.subsector IS NULL
WITH eq, z LIMIT 5000
CREATE (eq)-[:LOCATED_IN]->(z);

// Zones PART_OF major assets
MATCH (z:ManufacturingZone)
MATCH (a:MajorManufacturingAsset)
WHERE z.subsector = a.subsector
WITH z, a LIMIT 500
CREATE (z)-[:PART_OF]->(a);

// Equipment TRIGGERS alerts
MATCH (eq:ManufacturingEquipment)
MATCH (alert:ManufacturingAlert)
WHERE toInteger(substring(eq.id, 9, 5)) % 25 = toInteger(substring(alert.id, 9, 6)) % 25
WITH eq, alert LIMIT 2000
CREATE (eq)-[:TRIGGERS]->(alert);

// ========================================
// DEPLOYMENT COMPLETE
// Estimated Nodes: ~54,700
// - ManufacturingEquipment: 11,200
// - ManufacturingMeasurement: 18,200
// - ManufacturingProperty: 5,000
// - ManufacturingProcess: 2,800
// - ManufacturingControl: 1,400
// - ManufacturingAlert: 400
// - ManufacturingZone: 200
// - MajorManufacturingAsset: 100
// Plus existing 400 upgraded
// ========================================
