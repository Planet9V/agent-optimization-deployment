// ═══════════════════════════════════════════════════════════════════════════════
// COMMUNICATIONS SECTOR - COMPLETE IMPLEMENTATION
// Universal Location Architecture with Neural Learning from Energy Pilot
// ═══════════════════════════════════════════════════════════════════════════════

// PHASE 1: CREATE FACILITIES (40 Communications Facilities with Real Coordinates)
// ═══════════════════════════════════════════════════════════════════════════════

// Tech Hubs - San Francisco Bay Area (10 facilities)
CREATE (f1:Facility {
  facilityId: 'FAC-COM-DATACENTER-SF-001',
  facilityType: 'DATA_CENTER',
  facilityName: 'Bay Area Tier 3 Data Center',
  sector: 'COMMUNICATIONS',
  latitude: 37.7749,
  longitude: -122.4194,
  city: 'San Francisco',
  state: 'CA',
  country: 'USA',
  tier: 'TIER_3',
  capacity_racks: 500,
  power_redundancy: '2N',
  compliance: ['SOC2', 'ISO27001', 'PCI-DSS']
});

CREATE (f2:Facility {
  facilityId: 'FAC-COM-CELL-TOWER-SF-002',
  facilityType: 'CELL_TOWER',
  facilityName: 'San Francisco Downtown Cell Site',
  sector: 'COMMUNICATIONS',
  latitude: 37.7897,
  longitude: -122.3972,
  city: 'San Francisco',
  state: 'CA',
  country: 'USA',
  tower_height_meters: 50,
  coverage_radius_km: 5,
  frequency_bands: ['700MHz', '2.5GHz', '3.5GHz', '28GHz']
});

CREATE (f3:Facility {
  facilityId: 'FAC-COM-BROADCAST-SF-003',
  facilityType: 'BROADCAST_TOWER',
  facilityName: 'Sutro Tower Broadcast Facility',
  sector: 'COMMUNICATIONS',
  latitude: 37.7552,
  longitude: -122.4528,
  city: 'San Francisco',
  state: 'CA',
  country: 'USA',
  tower_height_meters: 298,
  broadcast_power_kw: 100,
  services: ['TV', 'FM_RADIO', 'EMERGENCY_COMMS']
});

CREATE (f4:Facility {
  facilityId: 'FAC-COM-DATACENTER-SJ-004',
  facilityType: 'DATA_CENTER',
  facilityName: 'San Jose Hyperscale Data Center',
  sector: 'COMMUNICATIONS',
  latitude: 37.3382,
  longitude: -121.8863,
  city: 'San Jose',
  state: 'CA',
  country: 'USA',
  tier: 'TIER_4',
  capacity_racks: 2000,
  power_redundancy: '2N+1',
  compliance: ['SOC2', 'ISO27001', 'HIPAA', 'PCI-DSS']
});

CREATE (f5:Facility {
  facilityId: 'FAC-COM-NOC-PA-005',
  facilityType: 'NETWORK_OPERATIONS_CENTER',
  facilityName: 'Palo Alto Network Operations Center',
  sector: 'COMMUNICATIONS',
  latitude: 37.4419,
  longitude: -122.1430,
  city: 'Palo Alto',
  state: 'CA',
  country: 'USA',
  staffing: '24x7',
  monitored_networks: 15,
  incident_response_sla_minutes: 15
});

CREATE (f6:Facility {
  facilityId: 'FAC-COM-SWITCHING-OAK-006',
  facilityType: 'TELECOMMUNICATIONS_SWITCHING_CENTER',
  facilityName: 'Oakland Central Office',
  sector: 'COMMUNICATIONS',
  latitude: 37.8044,
  longitude: -122.2712,
  city: 'Oakland',
  state: 'CA',
  country: 'USA',
  switching_capacity_calls: 100000,
  fiber_terminations: 50000,
  legacy_pstn: true
});

CREATE (f7:Facility {
  facilityId: 'FAC-COM-CELL-TOWER-SJ-007',
  facilityType: 'CELL_TOWER',
  facilityName: 'San Jose 5G Macro Site',
  sector: 'COMMUNICATIONS',
  latitude: 37.3541,
  longitude: -121.9552,
  city: 'San Jose',
  state: 'CA',
  country: 'USA',
  tower_height_meters: 45,
  coverage_radius_km: 3,
  frequency_bands: ['3.5GHz', '28GHz', '39GHz'],
  technology: '5G_NR'
});

CREATE (f8:Facility {
  facilityId: 'FAC-COM-DATACENTER-FRE-008',
  facilityType: 'DATA_CENTER',
  facilityName: 'Fremont Colocation Facility',
  sector: 'COMMUNICATIONS',
  latitude: 37.5485,
  longitude: -121.9886,
  city: 'Fremont',
  state: 'CA',
  country: 'USA',
  tier: 'TIER_3',
  capacity_racks: 800,
  power_redundancy: 'N+1',
  compliance: ['SOC2', 'ISO27001']
});

CREATE (f9:Facility {
  facilityId: 'FAC-COM-BROADCAST-SAC-009',
  facilityType: 'BROADCAST_TOWER',
  facilityName: 'Sacramento Regional Broadcast Site',
  sector: 'COMMUNICATIONS',
  latitude: 38.5816,
  longitude: -121.4944,
  city: 'Sacramento',
  state: 'CA',
  country: 'USA',
  tower_height_meters: 120,
  broadcast_power_kw: 50,
  services: ['TV', 'FM_RADIO']
});

CREATE (f10:Facility {
  facilityId: 'FAC-COM-CELL-TOWER-BER-010',
  facilityType: 'CELL_TOWER',
  facilityName: 'Berkeley Hills Cell Site',
  sector: 'COMMUNICATIONS',
  latitude: 37.8716,
  longitude: -122.2477,
  city: 'Berkeley',
  state: 'CA',
  country: 'USA',
  tower_height_meters: 40,
  coverage_radius_km: 6,
  frequency_bands: ['700MHz', '1.9GHz', '2.5GHz']
});

// Texas - Austin (5 facilities)
CREATE (f11:Facility {
  facilityId: 'FAC-COM-DATACENTER-AUS-011',
  facilityType: 'DATA_CENTER',
  facilityName: 'Austin Tech Ridge Data Center',
  sector: 'COMMUNICATIONS',
  latitude: 30.2672,
  longitude: -97.7431,
  city: 'Austin',
  state: 'TX',
  country: 'USA',
  tier: 'TIER_3',
  capacity_racks: 600,
  power_redundancy: '2N',
  compliance: ['SOC2', 'ISO27001', 'HIPAA']
});

CREATE (f12:Facility {
  facilityId: 'FAC-COM-NOC-AUS-012',
  facilityType: 'NETWORK_OPERATIONS_CENTER',
  facilityName: 'Austin Regional NOC',
  sector: 'COMMUNICATIONS',
  latitude: 30.3072,
  longitude: -97.7559,
  city: 'Austin',
  state: 'TX',
  country: 'USA',
  staffing: '24x7',
  monitored_networks: 10,
  incident_response_sla_minutes: 20
});

CREATE (f13:Facility {
  facilityId: 'FAC-COM-CELL-TOWER-AUS-013',
  facilityType: 'CELL_TOWER',
  facilityName: 'Austin Downtown 5G Site',
  sector: 'COMMUNICATIONS',
  latitude: 30.2711,
  longitude: -97.7437,
  city: 'Austin',
  state: 'TX',
  country: 'USA',
  tower_height_meters: 35,
  coverage_radius_km: 2,
  frequency_bands: ['3.5GHz', '28GHz'],
  technology: '5G_NR'
});

CREATE (f14:Facility {
  facilityId: 'FAC-COM-SWITCHING-AUS-014',
  facilityType: 'TELECOMMUNICATIONS_SWITCHING_CENTER',
  facilityName: 'Austin Central Exchange',
  sector: 'COMMUNICATIONS',
  latitude: 30.2849,
  longitude: -97.7341,
  city: 'Austin',
  state: 'TX',
  country: 'USA',
  switching_capacity_calls: 75000,
  fiber_terminations: 30000,
  legacy_pstn: true
});

CREATE (f15:Facility {
  facilityId: 'FAC-COM-BROADCAST-AUS-015',
  facilityType: 'BROADCAST_TOWER',
  facilityName: 'Mount Bonnell Broadcast Tower',
  sector: 'COMMUNICATIONS',
  latitude: 30.3215,
  longitude: -97.7725,
  city: 'Austin',
  state: 'TX',
  country: 'USA',
  tower_height_meters: 80,
  broadcast_power_kw: 30,
  services: ['TV', 'FM_RADIO']
});

// Pacific Northwest - Seattle (5 facilities)
CREATE (f16:Facility {
  facilityId: 'FAC-COM-DATACENTER-SEA-016',
  facilityType: 'DATA_CENTER',
  facilityName: 'Seattle Tier 4 Data Center',
  sector: 'COMMUNICATIONS',
  latitude: 47.6062,
  longitude: -122.3321,
  city: 'Seattle',
  state: 'WA',
  country: 'USA',
  tier: 'TIER_4',
  capacity_racks: 1500,
  power_redundancy: '2N+1',
  compliance: ['SOC2', 'ISO27001', 'PCI-DSS', 'HIPAA']
});

CREATE (f17:Facility {
  facilityId: 'FAC-COM-CELL-TOWER-SEA-017',
  facilityType: 'CELL_TOWER',
  facilityName: 'Seattle Space Needle Cell Site',
  sector: 'COMMUNICATIONS',
  latitude: 47.6205,
  longitude: -122.3493,
  city: 'Seattle',
  state: 'WA',
  country: 'USA',
  tower_height_meters: 60,
  coverage_radius_km: 7,
  frequency_bands: ['600MHz', '2.5GHz', '3.5GHz', '28GHz']
});

CREATE (f18:Facility {
  facilityId: 'FAC-COM-NOC-SEA-018',
  facilityType: 'NETWORK_OPERATIONS_CENTER',
  facilityName: 'Seattle Pacific NOC',
  sector: 'COMMUNICATIONS',
  latitude: 47.6145,
  longitude: -122.3418,
  city: 'Seattle',
  state: 'WA',
  country: 'USA',
  staffing: '24x7',
  monitored_networks: 20,
  incident_response_sla_minutes: 10
});

CREATE (f19:Facility {
  facilityId: 'FAC-COM-SWITCHING-SEA-019',
  facilityType: 'TELECOMMUNICATIONS_SWITCHING_CENTER',
  facilityName: 'Seattle Westin Building Exchange',
  sector: 'COMMUNICATIONS',
  latitude: 47.6097,
  longitude: -122.3365,
  city: 'Seattle',
  state: 'WA',
  country: 'USA',
  switching_capacity_calls: 150000,
  fiber_terminations: 100000,
  legacy_pstn: false,
  major_internet_exchange: true
});

CREATE (f20:Facility {
  facilityId: 'FAC-COM-DATACENTER-POR-020',
  facilityType: 'DATA_CENTER',
  facilityName: 'Portland Rivergate Data Center',
  sector: 'COMMUNICATIONS',
  latitude: 45.5152,
  longitude: -122.6784,
  city: 'Portland',
  state: 'OR',
  country: 'USA',
  tier: 'TIER_3',
  capacity_racks: 400,
  power_redundancy: 'N+1',
  compliance: ['SOC2', 'ISO27001']
});

// Data Center Hubs - Virginia (5 facilities)
CREATE (f21:Facility {
  facilityId: 'FAC-COM-DATACENTER-ASH-021',
  facilityType: 'DATA_CENTER',
  facilityName: 'Ashburn Mega Data Center Alpha',
  sector: 'COMMUNICATIONS',
  latitude: 39.0438,
  longitude: -77.4874,
  city: 'Ashburn',
  state: 'VA',
  country: 'USA',
  tier: 'TIER_4',
  capacity_racks: 5000,
  power_redundancy: '2N+1',
  compliance: ['SOC2', 'ISO27001', 'PCI-DSS', 'FISMA', 'HIPAA']
});

CREATE (f22:Facility {
  facilityId: 'FAC-COM-DATACENTER-ASH-022',
  facilityType: 'DATA_CENTER',
  facilityName: 'Ashburn Mega Data Center Beta',
  sector: 'COMMUNICATIONS',
  latitude: 39.0519,
  longitude: -77.4702,
  city: 'Ashburn',
  state: 'VA',
  country: 'USA',
  tier: 'TIER_4',
  capacity_racks: 4500,
  power_redundancy: '2N+1',
  compliance: ['SOC2', 'ISO27001', 'PCI-DSS', 'FISMA']
});

CREATE (f23:Facility {
  facilityId: 'FAC-COM-NOC-ASH-023',
  facilityType: 'NETWORK_OPERATIONS_CENTER',
  facilityName: 'Ashburn Internet Exchange NOC',
  sector: 'COMMUNICATIONS',
  latitude: 39.0366,
  longitude: -77.4977,
  city: 'Ashburn',
  state: 'VA',
  country: 'USA',
  staffing: '24x7',
  monitored_networks: 50,
  incident_response_sla_minutes: 5,
  major_internet_exchange: true
});

CREATE (f24:Facility {
  facilityId: 'FAC-COM-SWITCHING-ASH-024',
  facilityType: 'TELECOMMUNICATIONS_SWITCHING_CENTER',
  facilityName: 'Ashburn Carrier Hotel',
  sector: 'COMMUNICATIONS',
  latitude: 39.0399,
  longitude: -77.4812,
  city: 'Ashburn',
  state: 'VA',
  country: 'USA',
  switching_capacity_calls: 200000,
  fiber_terminations: 150000,
  legacy_pstn: false,
  carriers_present: 25
});

CREATE (f25:Facility {
  facilityId: 'FAC-COM-CELL-TOWER-ASH-025',
  facilityType: 'CELL_TOWER',
  facilityName: 'Ashburn 5G Small Cell Network Hub',
  sector: 'COMMUNICATIONS',
  latitude: 39.0470,
  longitude: -77.4894,
  city: 'Ashburn',
  state: 'VA',
  country: 'USA',
  tower_height_meters: 25,
  coverage_radius_km: 1,
  frequency_bands: ['3.5GHz', '28GHz', '39GHz'],
  technology: '5G_NR',
  small_cell: true
});

// Data Center Hubs - North Carolina (3 facilities)
CREATE (f26:Facility {
  facilityId: 'FAC-COM-DATACENTER-CLT-026',
  facilityType: 'DATA_CENTER',
  facilityName: 'Charlotte Enterprise Data Center',
  sector: 'COMMUNICATIONS',
  latitude: 35.2271,
  longitude: -80.8431,
  city: 'Charlotte',
  state: 'NC',
  country: 'USA',
  tier: 'TIER_3',
  capacity_racks: 1000,
  power_redundancy: '2N',
  compliance: ['SOC2', 'ISO27001', 'PCI-DSS']
});

CREATE (f27:Facility {
  facilityId: 'FAC-COM-DATACENTER-RAL-027',
  facilityType: 'DATA_CENTER',
  facilityName: 'Raleigh Research Triangle Data Center',
  sector: 'COMMUNICATIONS',
  latitude: 35.7796,
  longitude: -78.6382,
  city: 'Raleigh',
  state: 'NC',
  country: 'USA',
  tier: 'TIER_3',
  capacity_racks: 800,
  power_redundancy: 'N+1',
  compliance: ['SOC2', 'ISO27001', 'HIPAA']
});

CREATE (f28:Facility {
  facilityId: 'FAC-COM-NOC-CLT-028',
  facilityType: 'NETWORK_OPERATIONS_CENTER',
  facilityName: 'Charlotte Regional NOC',
  sector: 'COMMUNICATIONS',
  latitude: 35.2220,
  longitude: -80.8433,
  city: 'Charlotte',
  state: 'NC',
  country: 'USA',
  staffing: '24x7',
  monitored_networks: 12,
  incident_response_sla_minutes: 15
});

// Major Cities - New York (4 facilities)
CREATE (f29:Facility {
  facilityId: 'FAC-COM-DATACENTER-NYC-029',
  facilityType: 'DATA_CENTER',
  facilityName: 'Manhattan Financial District Data Center',
  sector: 'COMMUNICATIONS',
  latitude: 40.7074,
  longitude: -74.0113,
  city: 'New York',
  state: 'NY',
  country: 'USA',
  tier: 'TIER_4',
  capacity_racks: 3000,
  power_redundancy: '2N+1',
  compliance: ['SOC2', 'ISO27001', 'PCI-DSS', 'NYDFS']
});

CREATE (f30:Facility {
  facilityId: 'FAC-COM-CELL-TOWER-NYC-030',
  facilityType: 'CELL_TOWER',
  facilityName: 'Empire State Building Cell Site',
  sector: 'COMMUNICATIONS',
  latitude: 40.7484,
  longitude: -73.9857,
  city: 'New York',
  state: 'NY',
  country: 'USA',
  tower_height_meters: 70,
  coverage_radius_km: 10,
  frequency_bands: ['600MHz', '2.5GHz', '3.5GHz', '28GHz']
});

CREATE (f31:Facility {
  facilityId: 'FAC-COM-NOC-NYC-031',
  facilityType: 'NETWORK_OPERATIONS_CENTER',
  facilityName: 'New York Metro NOC',
  sector: 'COMMUNICATIONS',
  latitude: 40.7589,
  longitude: -73.9851,
  city: 'New York',
  state: 'NY',
  country: 'USA',
  staffing: '24x7',
  monitored_networks: 30,
  incident_response_sla_minutes: 5
});

CREATE (f32:Facility {
  facilityId: 'FAC-COM-SWITCHING-NYC-032',
  facilityType: 'TELECOMMUNICATIONS_SWITCHING_CENTER',
  facilityName: '60 Hudson Street Carrier Hotel',
  sector: 'COMMUNICATIONS',
  latitude: 40.7188,
  longitude: -74.0089,
  city: 'New York',
  state: 'NY',
  country: 'USA',
  switching_capacity_calls: 250000,
  fiber_terminations: 200000,
  legacy_pstn: false,
  carriers_present: 50,
  major_internet_exchange: true
});

// Major Cities - Chicago (3 facilities)
CREATE (f33:Facility {
  facilityId: 'FAC-COM-DATACENTER-CHI-033',
  facilityType: 'DATA_CENTER',
  facilityName: 'Chicago Loop Data Center',
  sector: 'COMMUNICATIONS',
  latitude: 41.8781,
  longitude: -87.6298,
  city: 'Chicago',
  state: 'IL',
  country: 'USA',
  tier: 'TIER_3',
  capacity_racks: 1200,
  power_redundancy: '2N',
  compliance: ['SOC2', 'ISO27001', 'PCI-DSS']
});

CREATE (f34:Facility {
  facilityId: 'FAC-COM-NOC-CHI-034',
  facilityType: 'NETWORK_OPERATIONS_CENTER',
  facilityName: 'Chicago Central NOC',
  sector: 'COMMUNICATIONS',
  latitude: 41.8827,
  longitude: -87.6233,
  city: 'Chicago',
  state: 'IL',
  country: 'USA',
  staffing: '24x7',
  monitored_networks: 18,
  incident_response_sla_minutes: 10
});

CREATE (f35:Facility {
  facilityId: 'FAC-COM-CELL-TOWER-CHI-035',
  facilityType: 'CELL_TOWER',
  facilityName: 'Willis Tower Cell Site',
  sector: 'COMMUNICATIONS',
  latitude: 41.8789,
  longitude: -87.6359,
  city: 'Chicago',
  state: 'IL',
  country: 'USA',
  tower_height_meters: 80,
  coverage_radius_km: 12,
  frequency_bands: ['600MHz', '1.9GHz', '2.5GHz', '3.5GHz']
});

// Major Cities - Los Angeles (3 facilities)
CREATE (f36:Facility {
  facilityId: 'FAC-COM-DATACENTER-LA-036',
  facilityType: 'DATA_CENTER',
  facilityName: 'Los Angeles Downtown Data Center',
  sector: 'COMMUNICATIONS',
  latitude: 34.0522,
  longitude: -118.2437,
  city: 'Los Angeles',
  state: 'CA',
  country: 'USA',
  tier: 'TIER_3',
  capacity_racks: 900,
  power_redundancy: 'N+1',
  compliance: ['SOC2', 'ISO27001', 'PCI-DSS']
});

CREATE (f37:Facility {
  facilityId: 'FAC-COM-CELL-TOWER-LA-037',
  facilityType: 'CELL_TOWER',
  facilityName: 'Hollywood Hills Cell Site',
  sector: 'COMMUNICATIONS',
  latitude: 34.1341,
  longitude: -118.3215,
  city: 'Los Angeles',
  state: 'CA',
  country: 'USA',
  tower_height_meters: 55,
  coverage_radius_km: 8,
  frequency_bands: ['700MHz', '2.5GHz', '3.5GHz']
});

CREATE (f38:Facility {
  facilityId: 'FAC-COM-BROADCAST-LA-038',
  facilityType: 'BROADCAST_TOWER',
  facilityName: 'Mount Wilson Broadcast Complex',
  sector: 'COMMUNICATIONS',
  latitude: 34.2246,
  longitude: -118.0574,
  city: 'Los Angeles',
  state: 'CA',
  country: 'USA',
  tower_height_meters: 150,
  broadcast_power_kw: 200,
  services: ['TV', 'FM_RADIO', 'EMERGENCY_COMMS']
});

// Specialized Facilities (2 facilities)
CREATE (f39:Facility {
  facilityId: 'FAC-COM-SWITCHING-DEN-039',
  facilityType: 'TELECOMMUNICATIONS_SWITCHING_CENTER',
  facilityName: 'Denver Regional Exchange',
  sector: 'COMMUNICATIONS',
  latitude: 39.7392,
  longitude: -104.9903,
  city: 'Denver',
  state: 'CO',
  country: 'USA',
  switching_capacity_calls: 80000,
  fiber_terminations: 40000,
  legacy_pstn: true
});

CREATE (f40:Facility {
  facilityId: 'FAC-COM-BROADCAST-MIA-040',
  facilityType: 'BROADCAST_TOWER',
  facilityName: 'Miami International Broadcast Tower',
  sector: 'COMMUNICATIONS',
  latitude: 25.7617,
  longitude: -80.1918,
  city: 'Miami',
  state: 'FL',
  country: 'USA',
  tower_height_meters: 100,
  broadcast_power_kw: 75,
  services: ['TV', 'FM_RADIO', 'EMERGENCY_COMMS']
});

// ═══════════════════════════════════════════════════════════════════════════════
// PHASE 2: CREATE AND ENRICH EQUIPMENT (300 Communications Equipment Nodes)
// ═══════════════════════════════════════════════════════════════════════════════

// Data Center Equipment - Routers (50 nodes)
UNWIND range(1, 50) AS idx
CREATE (eq:Equipment {
  equipmentId: 'COM-ROUTER-' + toString(idx),
  equipmentType: 'ROUTER',
  sector: 'COMMUNICATIONS',
  manufacturer: CASE idx % 3 WHEN 0 THEN 'Cisco' WHEN 1 THEN 'Juniper' ELSE 'Arista' END,
  model: CASE idx % 3 WHEN 0 THEN 'ASR-9000' WHEN 1 THEN 'MX960' ELSE '7500R3' END,
  capacity_gbps: CASE idx % 4 WHEN 0 THEN 100 WHEN 1 THEN 400 WHEN 2 THEN 800 ELSE 1600 END,
  port_count: CASE idx % 3 WHEN 0 THEN 48 WHEN 1 THEN 96 ELSE 144 END,
  routing_protocols: ['BGP', 'OSPF', 'IS-IS', 'MPLS'],
  criticality: CASE idx % 3 WHEN 0 THEN 'CRITICAL' ELSE 'HIGH' END,
  status: 'OPERATIONAL',
  facilityId: CASE
    WHEN idx <= 10 THEN 'FAC-COM-DATACENTER-SF-001'
    WHEN idx <= 18 THEN 'FAC-COM-DATACENTER-SJ-004'
    WHEN idx <= 25 THEN 'FAC-COM-DATACENTER-ASH-021'
    WHEN idx <= 32 THEN 'FAC-COM-DATACENTER-ASH-022'
    WHEN idx <= 38 THEN 'FAC-COM-DATACENTER-NYC-029'
    WHEN idx <= 44 THEN 'FAC-COM-DATACENTER-SEA-016'
    ELSE 'FAC-COM-DATACENTER-CHI-033'
  END
});

// Data Center Equipment - Switches (50 nodes)
UNWIND range(1, 50) AS idx
CREATE (eq:Equipment {
  equipmentId: 'COM-SWITCH-' + toString(idx),
  equipmentType: 'SWITCH',
  sector: 'COMMUNICATIONS',
  manufacturer: CASE idx % 3 WHEN 0 THEN 'Cisco' WHEN 1 THEN 'Arista' ELSE 'Juniper' END,
  model: CASE idx % 3 WHEN 0 THEN 'Nexus-9000' WHEN 1 THEN '7280R3' ELSE 'QFX10000' END,
  capacity_gbps: CASE idx % 4 WHEN 0 THEN 100 WHEN 1 THEN 400 WHEN 2 THEN 800 ELSE 1600 END,
  port_count: CASE idx % 3 WHEN 0 THEN 48 WHEN 1 THEN 96 ELSE 144 END,
  vlan_support: true,
  layer: 'LAYER_3',
  criticality: 'HIGH',
  status: 'OPERATIONAL',
  facilityId: CASE
    WHEN idx <= 10 THEN 'FAC-COM-DATACENTER-SF-001'
    WHEN idx <= 18 THEN 'FAC-COM-DATACENTER-SJ-004'
    WHEN idx <= 25 THEN 'FAC-COM-DATACENTER-ASH-021'
    WHEN idx <= 32 THEN 'FAC-COM-DATACENTER-ASH-022'
    WHEN idx <= 38 THEN 'FAC-COM-DATACENTER-NYC-029'
    WHEN idx <= 44 THEN 'FAC-COM-DATACENTER-SEA-016'
    ELSE 'FAC-COM-DATACENTER-CHI-033'
  END
});

// Data Center Equipment - Servers (60 nodes)
UNWIND range(1, 60) AS idx
CREATE (eq:Equipment {
  equipmentId: 'COM-SERVER-' + toString(idx),
  equipmentType: 'SERVER',
  sector: 'COMMUNICATIONS',
  manufacturer: CASE idx % 4 WHEN 0 THEN 'Dell' WHEN 1 THEN 'HPE' WHEN 2 THEN 'Supermicro' ELSE 'Lenovo' END,
  model: CASE idx % 4 WHEN 0 THEN 'PowerEdge-R750' WHEN 1 THEN 'ProLiant-DL380' WHEN 2 THEN 'SYS-2029U' ELSE 'ThinkSystem-SR650' END,
  cpu_cores: CASE idx % 5 WHEN 0 THEN 32 WHEN 1 THEN 64 WHEN 2 THEN 96 WHEN 3 THEN 128 ELSE 256 END,
  memory_gb: CASE idx % 5 WHEN 0 THEN 256 WHEN 1 THEN 512 WHEN 2 THEN 1024 WHEN 3 THEN 2048 ELSE 4096 END,
  storage_tb: CASE idx % 4 WHEN 0 THEN 10 WHEN 1 THEN 20 WHEN 2 THEN 50 ELSE 100 END,
  virtualization: CASE idx % 2 WHEN 0 THEN 'VMware_ESXi' ELSE 'KVM' END,
  workload: CASE idx % 5 WHEN 0 THEN 'WEB_SERVER' WHEN 1 THEN 'DATABASE' WHEN 2 THEN 'APPLICATION' WHEN 3 THEN 'CACHING' ELSE 'CDN' END,
  criticality: CASE idx % 3 WHEN 0 THEN 'CRITICAL' ELSE 'HIGH' END,
  status: 'OPERATIONAL',
  facilityId: CASE
    WHEN idx <= 12 THEN 'FAC-COM-DATACENTER-SF-001'
    WHEN idx <= 22 THEN 'FAC-COM-DATACENTER-SJ-004'
    WHEN idx <= 30 THEN 'FAC-COM-DATACENTER-ASH-021'
    WHEN idx <= 38 THEN 'FAC-COM-DATACENTER-ASH-022'
    WHEN idx <= 45 THEN 'FAC-COM-DATACENTER-NYC-029'
    WHEN idx <= 52 THEN 'FAC-COM-DATACENTER-SEA-016'
    ELSE 'FAC-COM-DATACENTER-CHI-033'
  END
});

// Cell Tower Equipment - Antennas (40 nodes)
UNWIND range(1, 40) AS idx
CREATE (eq:Equipment {
  equipmentId: 'COM-ANTENNA-' + toString(idx),
  equipmentType: 'ANTENNA',
  sector: 'COMMUNICATIONS',
  manufacturer: CASE idx % 3 WHEN 0 THEN 'Ericsson' WHEN 1 THEN 'Nokia' ELSE 'Samsung' END,
  model: CASE idx % 3 WHEN 0 THEN 'AIR-6449' WHEN 1 THEN 'AEHC' ELSE '5G-Massive-MIMO' END,
  frequency_bands: CASE idx % 4
    WHEN 0 THEN ['700MHz', '1.9GHz']
    WHEN 1 THEN ['2.5GHz', '3.5GHz']
    WHEN 2 THEN ['3.5GHz', '28GHz']
    ELSE ['28GHz', '39GHz']
  END,
  antenna_type: CASE idx % 3 WHEN 0 THEN 'PANEL' WHEN 1 THEN 'MIMO' ELSE 'MASSIVE_MIMO' END,
  gain_dbi: CASE idx % 3 WHEN 0 THEN 15 WHEN 1 THEN 18 ELSE 21 END,
  technology: CASE idx % 3 WHEN 0 THEN 'LTE' WHEN 1 THEN '5G_NR' ELSE '5G_NR_MMWAVE' END,
  criticality: 'HIGH',
  status: 'OPERATIONAL',
  facilityId: CASE
    WHEN idx <= 5 THEN 'FAC-COM-CELL-TOWER-SF-002'
    WHEN idx <= 8 THEN 'FAC-COM-CELL-TOWER-SJ-007'
    WHEN idx <= 11 THEN 'FAC-COM-CELL-TOWER-BER-010'
    WHEN idx <= 14 THEN 'FAC-COM-CELL-TOWER-AUS-013'
    WHEN idx <= 18 THEN 'FAC-COM-CELL-TOWER-SEA-017'
    WHEN idx <= 21 THEN 'FAC-COM-CELL-TOWER-ASH-025'
    WHEN idx <= 26 THEN 'FAC-COM-CELL-TOWER-NYC-030'
    WHEN idx <= 31 THEN 'FAC-COM-CELL-TOWER-CHI-035'
    ELSE 'FAC-COM-CELL-TOWER-LA-037'
  END
});

// Cell Tower Equipment - Base Stations (30 nodes)
UNWIND range(1, 30) AS idx
CREATE (eq:Equipment {
  equipmentId: 'COM-BASESTATION-' + toString(idx),
  equipmentType: 'BASE_STATION',
  sector: 'COMMUNICATIONS',
  manufacturer: CASE idx % 3 WHEN 0 THEN 'Ericsson' WHEN 1 THEN 'Nokia' ELSE 'Huawei' END,
  model: CASE idx % 3 WHEN 0 THEN 'Baseband-6630' WHEN 1 THEN 'AirScale-BS' ELSE 'BBU5900' END,
  technology: CASE idx % 3 WHEN 0 THEN 'LTE' WHEN 1 THEN '5G_NSA' ELSE '5G_SA' END,
  supported_users: CASE idx % 4 WHEN 0 THEN 500 WHEN 1 THEN 1000 WHEN 2 THEN 2000 ELSE 5000 END,
  spectrum_bandwidth_mhz: CASE idx % 3 WHEN 0 THEN 20 WHEN 1 THEN 100 ELSE 200 END,
  backhaul: CASE idx % 2 WHEN 0 THEN 'FIBER' ELSE 'MICROWAVE' END,
  criticality: 'CRITICAL',
  status: 'OPERATIONAL',
  facilityId: CASE
    WHEN idx <= 4 THEN 'FAC-COM-CELL-TOWER-SF-002'
    WHEN idx <= 7 THEN 'FAC-COM-CELL-TOWER-SJ-007'
    WHEN idx <= 10 THEN 'FAC-COM-CELL-TOWER-BER-010'
    WHEN idx <= 13 THEN 'FAC-COM-CELL-TOWER-AUS-013'
    WHEN idx <= 16 THEN 'FAC-COM-CELL-TOWER-SEA-017'
    WHEN idx <= 19 THEN 'FAC-COM-CELL-TOWER-ASH-025'
    WHEN idx <= 22 THEN 'FAC-COM-CELL-TOWER-NYC-030'
    WHEN idx <= 26 THEN 'FAC-COM-CELL-TOWER-CHI-035'
    ELSE 'FAC-COM-CELL-TOWER-LA-037'
  END
});

// Broadcast Equipment - Transmitters (20 nodes)
UNWIND range(1, 20) AS idx
CREATE (eq:Equipment {
  equipmentId: 'COM-TRANSMITTER-' + toString(idx),
  equipmentType: 'TRANSMITTER',
  sector: 'COMMUNICATIONS',
  manufacturer: CASE idx % 3 WHEN 0 THEN 'Harris' WHEN 1 THEN 'GatesAir' ELSE 'Rohde_Schwarz' END,
  model: CASE idx % 3 WHEN 0 THEN 'Maxiva-UAXT' WHEN 1 THEN 'Flexiva-FAX' ELSE 'THU9-UHF' END,
  broadcast_type: CASE idx % 4 WHEN 0 THEN 'TV' WHEN 1 THEN 'FM_RADIO' WHEN 2 THEN 'AM_RADIO' ELSE 'DIGITAL_TV' END,
  power_output_kw: CASE idx % 5 WHEN 0 THEN 10 WHEN 1 THEN 25 WHEN 2 THEN 50 WHEN 3 THEN 100 ELSE 200 END,
  frequency_mhz: CASE idx % 4 WHEN 0 THEN 88.5 WHEN 1 THEN 101.9 WHEN 2 THEN 540 ELSE 620 END,
  modulation: CASE idx % 3 WHEN 0 THEN 'FM' WHEN 1 THEN 'AM' ELSE 'ATSC_3.0' END,
  criticality: 'HIGH',
  status: 'OPERATIONAL',
  facilityId: CASE
    WHEN idx <= 4 THEN 'FAC-COM-BROADCAST-SF-003'
    WHEN idx <= 7 THEN 'FAC-COM-BROADCAST-SAC-009'
    WHEN idx <= 10 THEN 'FAC-COM-BROADCAST-AUS-015'
    WHEN idx <= 13 THEN 'FAC-COM-BROADCAST-LA-038'
    ELSE 'FAC-COM-BROADCAST-MIA-040'
  END
});

// NOC Equipment - Monitoring Systems (25 nodes)
UNWIND range(1, 25) AS idx
CREATE (eq:Equipment {
  equipmentId: 'COM-MONITOR-' + toString(idx),
  equipmentType: 'MONITORING_SYSTEM',
  sector: 'COMMUNICATIONS',
  manufacturer: CASE idx % 4 WHEN 0 THEN 'SolarWinds' WHEN 1 THEN 'PRTG' WHEN 2 THEN 'Zabbix' ELSE 'Nagios' END,
  model: CASE idx % 4 WHEN 0 THEN 'NPM' WHEN 1 THEN 'Network-Monitor' WHEN 2 THEN 'Enterprise' ELSE 'XI' END,
  monitored_devices: CASE idx % 5 WHEN 0 THEN 100 WHEN 1 THEN 500 WHEN 2 THEN 1000 WHEN 3 THEN 5000 ELSE 10000 END,
  metrics_collected: ['SNMP', 'NETFLOW', 'SYSLOG', 'PACKET_CAPTURE'],
  alerting: true,
  dashboard_enabled: true,
  retention_days: CASE idx % 3 WHEN 0 THEN 30 WHEN 1 THEN 90 ELSE 365 END,
  criticality: 'CRITICAL',
  status: 'OPERATIONAL',
  facilityId: CASE
    WHEN idx <= 5 THEN 'FAC-COM-NOC-PA-005'
    WHEN idx <= 9 THEN 'FAC-COM-NOC-AUS-012'
    WHEN idx <= 13 THEN 'FAC-COM-NOC-SEA-018'
    WHEN idx <= 17 THEN 'FAC-COM-NOC-ASH-023'
    WHEN idx <= 21 THEN 'FAC-COM-NOC-NYC-031'
    ELSE 'FAC-COM-NOC-CHI-034'
  END
});

// Switching Equipment - Optical Switches (25 nodes)
UNWIND range(1, 25) AS idx
CREATE (eq:Equipment {
  equipmentId: 'COM-OPTICAL-SWITCH-' + toString(idx),
  equipmentType: 'OPTICAL_SWITCH',
  sector: 'COMMUNICATIONS',
  manufacturer: CASE idx % 3 WHEN 0 THEN 'Ciena' WHEN 1 THEN 'Infinera' ELSE 'Nokia' END,
  model: CASE idx % 3 WHEN 0 THEN '6500-Packet-Optical' WHEN 1 THEN 'GX-Series' ELSE '1830-PSS' END,
  wavelengths: CASE idx % 4 WHEN 0 THEN 48 WHEN 1 THEN 96 WHEN 2 THEN 192 ELSE 384 END,
  capacity_tbps: CASE idx % 5 WHEN 0 THEN 1 WHEN 1 THEN 5 WHEN 2 THEN 10 WHEN 3 THEN 20 ELSE 50 END,
  technology: CASE idx % 2 WHEN 0 THEN 'DWDM' ELSE 'CWDM' END,
  reach_km: CASE idx % 4 WHEN 0 THEN 80 WHEN 1 THEN 500 WHEN 2 THEN 1000 ELSE 2000 END,
  criticality: 'CRITICAL',
  status: 'OPERATIONAL',
  facilityId: CASE
    WHEN idx <= 5 THEN 'FAC-COM-SWITCHING-OAK-006'
    WHEN idx <= 9 THEN 'FAC-COM-SWITCHING-AUS-014'
    WHEN idx <= 13 THEN 'FAC-COM-SWITCHING-SEA-019'
    WHEN idx <= 17 THEN 'FAC-COM-SWITCHING-ASH-024'
    WHEN idx <= 21 THEN 'FAC-COM-SWITCHING-NYC-032'
    ELSE 'FAC-COM-SWITCHING-DEN-039'
  END
});

// ═══════════════════════════════════════════════════════════════════════════════
// PHASE 3: CREATE RELATIONSHIPS (facilityId Matching)
// ═══════════════════════════════════════════════════════════════════════════════

// LOCATED_AT relationships using direct facilityId matching
MATCH (eq:Equipment)
WHERE eq.facilityId IS NOT NULL
  AND eq.equipmentId STARTS WITH 'COM-'
MATCH (f:Facility)
WHERE f.facilityId = eq.facilityId
MERGE (eq)-[:LOCATED_AT {
  relationship_type: 'PHYSICAL_LOCATION',
  created_date: date(),
  verified: true
}]->(f);

// ═══════════════════════════════════════════════════════════════════════════════
// PHASE 4: APPLY TAGS (5-Dimensional Tagging)
// ═══════════════════════════════════════════════════════════════════════════════

// 1. GEO_* Tags (Geographic)
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
MATCH (eq)-[:LOCATED_AT]->(f:Facility)
SET eq.tags = CASE
  WHEN eq.tags IS NULL THEN []
  ELSE eq.tags
END +
CASE
  WHEN f.state IN ['CA', 'OR', 'WA'] THEN ['GEO_WEST_COAST']
  WHEN f.state = 'TX' THEN ['GEO_TEXAS']
  WHEN f.state IN ['VA', 'NC'] THEN ['GEO_EAST_COAST_DC_HUB']
  WHEN f.state IN ['NY', 'IL'] THEN ['GEO_MAJOR_METRO']
  ELSE ['GEO_OTHER']
END;

// 2. OPS_* Tags (Operational)
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
SET eq.tags = eq.tags +
CASE eq.equipmentType
  WHEN 'ROUTER' THEN ['OPS_NETWORK_CORE']
  WHEN 'SWITCH' THEN ['OPS_NETWORK_DISTRIBUTION']
  WHEN 'SERVER' THEN ['OPS_COMPUTE']
  WHEN 'ANTENNA' THEN ['OPS_WIRELESS_ACCESS']
  WHEN 'BASE_STATION' THEN ['OPS_WIRELESS_CORE']
  WHEN 'TRANSMITTER' THEN ['OPS_BROADCAST']
  WHEN 'MONITORING_SYSTEM' THEN ['OPS_MANAGEMENT']
  WHEN 'OPTICAL_SWITCH' THEN ['OPS_TRANSPORT']
  ELSE ['OPS_GENERAL']
END;

// 3. REG_* Tags (Regulatory)
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
MATCH (eq)-[:LOCATED_AT]->(f:Facility)
SET eq.tags = eq.tags + ['REG_FCC_PART_15', 'REG_CISA_COMMUNICATIONS'];

// Add specific regulatory tags for wireless equipment
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
  AND eq.equipmentType IN ['ANTENNA', 'BASE_STATION', 'TRANSMITTER']
SET eq.tags = eq.tags + ['REG_FCC_WIRELESS_LICENSE'];

// 4. TECH_* Tags (Technology)
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
SET eq.tags = eq.tags +
CASE
  WHEN eq.technology IN ['5G_NR', '5G_SA', '5G_NSA'] THEN ['TECH_5G']
  WHEN eq.technology = 'LTE' THEN ['TECH_LTE']
  WHEN eq.technology IN ['DWDM', 'CWDM'] THEN ['TECH_OPTICAL']
  WHEN eq.workload IS NOT NULL THEN ['TECH_CLOUD_NATIVE']
  WHEN eq.virtualization IS NOT NULL THEN ['TECH_VIRTUALIZED']
  ELSE ['TECH_TRADITIONAL']
END;

// 5. TIME_* Tags (Temporal)
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
SET eq.tags = eq.tags + ['TIME_2025_Q4', 'TIME_OPERATIONAL'];

// ═══════════════════════════════════════════════════════════════════════════════
// VALIDATION QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

// Count facilities created
MATCH (f:Facility)
WHERE f.facilityId STARTS WITH 'FAC-COM-'
RETURN 'Facilities Created' as metric, count(f) as count;

// Count equipment created
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
RETURN 'Equipment Created' as metric, count(eq) as count;

// Count relationships
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'COM-'
RETURN 'LOCATED_AT Relationships' as metric, count(r) as count;

// Verify relationship coverage
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
OPTIONAL MATCH (eq)-[r:LOCATED_AT]->(f:Facility)
WITH count(eq) as total_equipment, count(r) as linked_equipment
RETURN 'Relationship Coverage' as metric,
       linked_equipment as linked,
       total_equipment as total,
       round(100.0 * linked_equipment / total_equipment, 2) as coverage_percent;

// Tag distribution
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'COM-'
UNWIND eq.tags as tag
RETURN substring(tag, 0, 4) as tag_category,
       count(*) as count
ORDER BY tag_category;

// Equipment by facility type
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'COM-'
RETURN f.facilityType as facility_type,
       count(eq) as equipment_count
ORDER BY equipment_count DESC;

// ═══════════════════════════════════════════════════════════════════════════════
// COMPLETION MESSAGE
// ═══════════════════════════════════════════════════════════════════════════════
