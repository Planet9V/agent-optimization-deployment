// ═══════════════════════════════════════════════════════════════
// LAYER 1: Physical Asset Layer
// Digital Twin: Component → Interface → System → Fleet
// Created: 2025-10-29
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: PhysicalAsset (Top-level container)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID (unique identifier)
//   name: string (human-readable name)
//   type: enum [BUILDING, VEHICLE, FACILITY, INFRASTRUCTURE, FLEET]
//   customer_namespace: string (e.g., "customer:ABC" or "shared:industry")
//   is_shared: boolean (true for industry models, false for customer-specific)
//   location: {lat: float, lon: float, address: string}
//   commissioning_date: date
//   operational_status: enum [OPERATIONAL, MAINTENANCE, DECOMMISSIONED]
// ───────────────────────────────────────────────────────────────

// Example: Water treatment plant (industry reference model)
CREATE (plant:PhysicalAsset {
  id: 'asset-water-treatment-ref-001',
  name: 'IEC 62443 Reference Water Treatment Plant',
  type: 'FACILITY',
  customer_namespace: 'shared:industry',
  is_shared: true,
  operational_status: 'OPERATIONAL'
});

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: Device (ICS/SCADA equipment, IT hardware)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   name: string
//   manufacturer: string
//   model: string
//   serialNumber: string
//   cpe: string (Common Platform Enumeration for vulnerability matching)
//   firmwareVersion: string
//   criticalityLevel: enum [LOW, MEDIUM, HIGH, CRITICAL]
//   deviceType: enum [PLC, HMI, RTU, SCADA_SERVER, WORKSTATION, SENSOR, ACTUATOR, NETWORK_SWITCH, FIREWALL]
//   customer_namespace: string
//   is_shared: boolean
//   installation_date: date
//   last_maintenance: date
// ───────────────────────────────────────────────────────────────

// Example: Siemens S7-1500 PLC controlling water treatment
CREATE (plc:Device {
  id: 'device-plc-siemens-s7-1500-001',
  name: 'Main Treatment Process PLC',
  manufacturer: 'Siemens',
  model: 'S7-1500',
  serialNumber: 'S7-1500-ABC123',
  cpe: 'cpe:2.3:h:siemens:simatic_s7-1500:2.9.2:*:*:*:*:*:*:*',
  firmwareVersion: '2.9.2',
  criticalityLevel: 'CRITICAL',
  deviceType: 'PLC',
  customer_namespace: 'shared:industry',
  is_shared: true
});

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: HardwareComponent (Modules, cards, interfaces)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   name: string
//   componentType: enum [CPU_MODULE, IO_MODULE, COMMUNICATION_MODULE, POWER_SUPPLY, NETWORK_CARD, SENSOR, ACTUATOR]
//   manufacturer: string
//   partNumber: string
//   cpe: string
//   firmwareVersion: string
//   interface_type: string (e.g., "Profibus", "Modbus TCP", "Ethernet/IP")
// ───────────────────────────────────────────────────────────────

// Example: Communication module on PLC
CREATE (comm_module:HardwareComponent {
  id: 'component-siemens-cm1542-001',
  name: 'Siemens CM 1542-5 Communication Module',
  componentType: 'COMMUNICATION_MODULE',
  manufacturer: 'Siemens',
  partNumber: '6GK7542-5DX00-0XE0',
  cpe: 'cpe:2.3:h:siemens:simatic_cm_1542-5:4.0.0:*:*:*:*:*:*:*',
  firmwareVersion: '4.0.0',
  interface_type: 'Profinet'
});

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: Location (Physical/Geographic placement)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   name: string
//   locationType: enum [BUILDING, ROOM, RACK, ZONE, GEOGRAPHIC]
//   coordinates: {lat: float, lon: float}
//   address: string
//   parent_location: UUID (for hierarchical locations)
// ───────────────────────────────────────────────────────────────

CREATE (control_room:Location {
  id: 'location-control-room-001',
  name: 'Main Control Room',
  locationType: 'ROOM',
  address: 'Building A, Floor 2, Room 201'
});

// ═══════════════════════════════════════════════════════════════
// RELATIONSHIP PATTERNS - Layer 1
// ═══════════════════════════════════════════════════════════════

// Physical containment hierarchy
CREATE (plant)-[:CONTAINS_DEVICE]->(plc);
CREATE (plc)-[:HAS_COMPONENT]->(comm_module);
CREATE (plc)-[:LOCATED_AT]->(control_room);

// ───────────────────────────────────────────────────────────────
// Multi-Hop Example: Train Car Component → Fleet
// ───────────────────────────────────────────────────────────────

// Component level
CREATE (brake_controller:HardwareComponent {
  id: 'component-brake-ecu-001',
  name: 'Electronic Brake Control Unit',
  componentType: 'CPU_MODULE',
  manufacturer: 'Knorr-Bremse',
  partNumber: 'CCB-II-001',
  cpe: 'cpe:2.3:h:knorr-bremse:ccb_ii:3.2.1:*:*:*:*:*:*:*',
  firmwareVersion: '3.2.1'
});

// Device level (train car subsystem)
CREATE (brake_system:Device {
  id: 'device-brake-system-car-001',
  name: 'Train Car #1 Brake System',
  manufacturer: 'Knorr-Bremse',
  model: 'CCB-II',
  deviceType: 'ACTUATOR',
  criticalityLevel: 'CRITICAL',
  customer_namespace: 'customer:RailOperator-XYZ'
});

// Train car level
CREATE (train_car:PhysicalAsset {
  id: 'asset-train-car-001',
  name: 'Passenger Car #1',
  type: 'VEHICLE',
  customer_namespace: 'customer:RailOperator-XYZ',
  is_shared: false
});

// Train consist level
CREATE (train_consist:PhysicalAsset {
  id: 'asset-train-consist-A',
  name: 'Train Consist A (10 cars)',
  type: 'VEHICLE',
  customer_namespace: 'customer:RailOperator-XYZ'
});

// Fleet level
CREATE (fleet:PhysicalAsset {
  id: 'asset-fleet-regional',
  name: 'Regional Rail Fleet (50 trains)',
  type: 'FLEET',
  customer_namespace: 'customer:RailOperator-XYZ'
});

// Build multi-hop hierarchy (20+ hops possible)
CREATE (brake_controller)-[:INSTALLED_IN]->(brake_system);
CREATE (brake_system)-[:PART_OF_SUBSYSTEM]->(train_car);
CREATE (train_car)-[:PART_OF_CONSIST]->(train_consist);
CREATE (train_consist)-[:PART_OF_FLEET]->(fleet);

// ═══════════════════════════════════════════════════════════════
// QUERY EXAMPLES - Multi-Hop Traversal
// ═══════════════════════════════════════════════════════════════

// Find all components in a fleet (5-hop query)
MATCH path = (comp:HardwareComponent)-[:INSTALLED_IN]->(:Device)
  -[:PART_OF_SUBSYSTEM]->(:PhysicalAsset)
  -[:PART_OF_CONSIST]->(:PhysicalAsset)
  -[:PART_OF_FLEET]->(fleet:PhysicalAsset {id: 'asset-fleet-regional'})
RETURN comp, length(path) AS hops;

// Find all devices at a specific criticality level in customer namespace
MATCH (d:Device {
  customer_namespace: 'customer:RailOperator-XYZ',
  criticalityLevel: 'CRITICAL'
})
RETURN d.name, d.manufacturer, d.model;

// ═══════════════════════════════════════════════════════════════
// VALIDATION METRICS
// ═══════════════════════════════════════════════════════════════

// Count devices by criticality level
MATCH (d:Device)
RETURN d.criticalityLevel AS criticality, count(d) AS device_count
ORDER BY device_count DESC;

// Verify customer namespace isolation
MATCH (n)
WHERE n.customer_namespace IS NOT NULL
RETURN DISTINCT n.customer_namespace AS namespace,
       labels(n) AS node_types,
       count(n) AS node_count;
