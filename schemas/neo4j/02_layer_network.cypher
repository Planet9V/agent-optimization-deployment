// ═══════════════════════════════════════════════════════════════
// LAYER 2: Network & Communication Layer
// IEC 62443 Security Zones & Conduits, Network Topology
// Created: 2025-10-29
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: SecurityZone (IEC 62443 zones)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   name: string
//   securityLevel: enum [SL1, SL2, SL3, SL4]
//   description: string
//   zone_type: enum [ENTERPRISE, DMZ, CONTROL, SAFETY, FIELD]
//   customer_namespace: string
// ───────────────────────────────────────────────────────────────

// Example: Water treatment plant security zones
CREATE (enterprise_zone:SecurityZone {
  id: 'zone-enterprise-001',
  name: 'Enterprise Network Zone',
  securityLevel: 'SL1',
  description: 'Corporate IT network with standard security controls',
  zone_type: 'ENTERPRISE',
  customer_namespace: 'shared:industry'
});

CREATE (dmz_zone:SecurityZone {
  id: 'zone-dmz-001',
  name: 'DMZ Zone',
  securityLevel: 'SL2',
  description: 'Demilitarized zone for external-facing services',
  zone_type: 'DMZ',
  customer_namespace: 'shared:industry'
});

CREATE (control_zone:SecurityZone {
  id: 'zone-control-001',
  name: 'Process Control Zone',
  securityLevel: 'SL3',
  description: 'SCADA/DCS control network with enhanced security',
  zone_type: 'CONTROL',
  customer_namespace: 'shared:industry'
});

CREATE (safety_zone:SecurityZone {
  id: 'zone-safety-001',
  name: 'Safety Instrumented System Zone',
  securityLevel: 'SL4',
  description: 'Safety-critical systems with highest security level',
  zone_type: 'SAFETY',
  customer_namespace: 'shared:industry'
});

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: Conduit (Zone-to-zone communication pathway)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   name: string
//   conduit_type: enum [FIREWALL, DATA_DIODE, UNIDIRECTIONAL_GATEWAY, VPN, AIR_GAP]
//   security_controls: string[]
//   authentication_required: boolean
//   encryption_enabled: boolean
// ───────────────────────────────────────────────────────────────

CREATE (firewall_conduit:Conduit {
  id: 'conduit-fw-enterprise-control',
  name: 'Enterprise to Control Firewall',
  conduit_type: 'FIREWALL',
  security_controls: ['Stateful inspection', 'Deep packet inspection', 'IDS/IPS'],
  authentication_required: true,
  encryption_enabled: true
});

CREATE (data_diode:Conduit {
  id: 'conduit-dd-control-safety',
  name: 'Control to Safety Data Diode',
  conduit_type: 'DATA_DIODE',
  security_controls: ['Unidirectional data flow', 'Protocol validation'],
  authentication_required: true,
  encryption_enabled: true
});

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: Network (Logical network segment)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   name: string
//   network_type: enum [LAN, VLAN, WAN, WIRELESS, FIELDBUS]
//   cidr: string (e.g., "192.168.1.0/24")
//   vlan_id: integer
//   protocol: enum [ETHERNET, PROFIBUS, MODBUS_TCP, ETHERNET_IP, OPC_UA]
// ───────────────────────────────────────────────────────────────

CREATE (control_vlan:Network {
  id: 'network-control-vlan-100',
  name: 'SCADA Control VLAN',
  network_type: 'VLAN',
  cidr: '10.100.0.0/24',
  vlan_id: 100,
  protocol: 'ETHERNET'
});

CREATE (profibus_network:Network {
  id: 'network-profibus-field',
  name: 'Profibus Field Network',
  network_type: 'FIELDBUS',
  protocol: 'PROFIBUS',
  vlan_id: null
});

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: NetworkInterface (Device network connection)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   name: string
//   interface_type: enum [ETHERNET, WIFI, SERIAL, PROFIBUS, MODBUS, CANBUS]
//   mac_address: string
//   ip_address: string
//   port: integer
//   status: enum [UP, DOWN, UNKNOWN]
// ───────────────────────────────────────────────────────────────

CREATE (plc_eth0:NetworkInterface {
  id: 'netif-plc-eth0',
  name: 'PLC Ethernet 0',
  interface_type: 'ETHERNET',
  mac_address: '00:1B:1B:12:34:56',
  ip_address: '10.100.0.10',
  port: 102,
  status: 'UP'
});

CREATE (plc_profibus:NetworkInterface {
  id: 'netif-plc-profibus',
  name: 'PLC Profibus Interface',
  interface_type: 'PROFIBUS',
  mac_address: null,
  ip_address: null,
  port: null,
  status: 'UP'
});

// ═══════════════════════════════════════════════════════════════
// RELATIONSHIP PATTERNS - Layer 2
// ═══════════════════════════════════════════════════════════════

// Security zone hierarchy
CREATE (control_zone)-[:COMMUNICATES_VIA]->(firewall_conduit)-[:TO_ZONE]->(enterprise_zone);
CREATE (safety_zone)-[:COMMUNICATES_VIA]->(data_diode)-[:TO_ZONE]->(control_zone);

// Network within zone
CREATE (control_vlan)-[:PART_OF]->(control_zone);
CREATE (profibus_network)-[:PART_OF]->(control_zone);

// Device interfaces to networks
MATCH (plc:Device {id: 'device-plc-siemens-s7-1500-001'})
CREATE (plc)-[:HAS_INTERFACE]->(plc_eth0);
CREATE (plc)-[:HAS_INTERFACE]->(plc_profibus);
CREATE (plc_eth0)-[:CONNECTED_TO]->(control_vlan);
CREATE (plc_profibus)-[:CONNECTED_TO]->(profibus_network);

// ═══════════════════════════════════════════════════════════════
// QUERY EXAMPLES - Network Topology Analysis
// ═══════════════════════════════════════════════════════════════

// Find all devices in a security zone
MATCH (zone:SecurityZone {name: 'Process Control Zone'})
  <-[:PART_OF]-(network:Network)
  <-[:CONNECTED_TO]-(netif:NetworkInterface)
  <-[:HAS_INTERFACE]-(device:Device)
RETURN zone.name AS security_zone,
       zone.securityLevel AS security_level,
       network.name AS network,
       device.name AS device,
       device.criticalityLevel AS criticality;

// Identify zone-to-zone communication paths
MATCH (zone1:SecurityZone)-[:COMMUNICATES_VIA]->(conduit:Conduit)
  -[:TO_ZONE]->(zone2:SecurityZone)
RETURN zone1.name AS source_zone,
       zone1.securityLevel AS source_level,
       conduit.name AS conduit,
       conduit.conduit_type AS conduit_type,
       zone2.name AS target_zone,
       zone2.securityLevel AS target_level;

// Find potential unauthorized zone crossings (no conduit)
MATCH (d1:Device)-[:HAS_INTERFACE]->(ni1:NetworkInterface)
  -[:CONNECTED_TO]->(n1:Network)-[:PART_OF]->(zone1:SecurityZone),
      (d2:Device)-[:HAS_INTERFACE]->(ni2:NetworkInterface)
  -[:CONNECTED_TO]->(n2:Network)-[:PART_OF]->(zone2:SecurityZone)
WHERE zone1 <> zone2
  AND NOT EXISTS {
    MATCH (zone1)-[:COMMUNICATES_VIA]->(:Conduit)-[:TO_ZONE]->(zone2)
  }
  AND (ni1)-[:CONNECTED_TO]-(ni2)
RETURN d1.name AS device1,
       zone1.name AS zone1_name,
       d2.name AS device2,
       zone2.name AS zone2_name,
       'POTENTIAL UNAUTHORIZED CROSSING' AS alert;
