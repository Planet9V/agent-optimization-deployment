// ═══════════════════════════════════════════════════════════════
// GAP-004 TRANSPORTATION SECTOR DEPLOYMENT
// ═══════════════════════════════════════════════════════════════
// Equipment: 200 nodes (EQ-TRANS-20001 to EQ-TRANS-20200)
// Facilities: 50 transportation hubs
// Relationships: 200 LOCATED_AT (4 equipment per facility)
// Tagging: 5-dimensional (GEO, OPS, REG, TECH, TIME)
// ═══════════════════════════════════════════════════════════════

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20001',
  name: 'Radar System Unit 1',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200001',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_GA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20002',
  name: 'Security Scanner Unit 2',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200002',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_GA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20003',
  name: 'Navigation Equipment Unit 3',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200003',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_GA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20004',
  name: 'Traffic Control System Unit 4',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200004',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_GA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20005',
  name: 'Radar System Unit 5',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200005',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_GA", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20006',
  name: 'Security Scanner Unit 6',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200006',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_GA", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20007',
  name: 'Navigation Equipment Unit 7',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200007',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_GA", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20008',
  name: 'Traffic Control System Unit 8',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200008',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_GA", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20009',
  name: 'Radar System Unit 9',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200009',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_MD", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20010',
  name: 'Security Scanner Unit 10',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200010',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_MD", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20011',
  name: 'Navigation Equipment Unit 11',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200011',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_MD", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20012',
  name: 'Traffic Control System Unit 12',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200012',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_MD", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20013',
  name: 'Radar System Unit 13',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200013',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_BRIDGE", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20014',
  name: 'Security Scanner Unit 14',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200014',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_BRIDGE", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20015',
  name: 'Navigation Equipment Unit 15',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200015',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_BRIDGE", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20016',
  name: 'Traffic Control System Unit 16',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200016',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_BRIDGE", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20017',
  name: 'Radar System Unit 17',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200017',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_MA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20018',
  name: 'Security Scanner Unit 18',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200018',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_MA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20019',
  name: 'Navigation Equipment Unit 19',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200019',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_MA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20020',
  name: 'Traffic Control System Unit 20',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200020',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_MA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20021',
  name: 'Radar System Unit 21',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200021',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_MA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20022',
  name: 'Security Scanner Unit 22',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200022',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_MA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20023',
  name: 'Navigation Equipment Unit 23',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200023',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_MA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20024',
  name: 'Traffic Control System Unit 24',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200024',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_MA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20025',
  name: 'Radar System Unit 25',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200025',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_SC", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20026',
  name: 'Security Scanner Unit 26',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200026',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_SC", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20027',
  name: 'Navigation Equipment Unit 27',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200027',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_SC", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20028',
  name: 'Traffic Control System Unit 28',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200028',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_SC", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20029',
  name: 'Radar System Unit 29',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200029',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20030',
  name: 'Security Scanner Unit 30',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200030',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20031',
  name: 'Navigation Equipment Unit 31',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200031',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20032',
  name: 'Traffic Control System Unit 32',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200032',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20033',
  name: 'Radar System Unit 33',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200033',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20034',
  name: 'Security Scanner Unit 34',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200034',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20035',
  name: 'Navigation Equipment Unit 35',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200035',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20036',
  name: 'Traffic Control System Unit 36',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200036',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20037',
  name: 'Radar System Unit 37',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200037',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20038',
  name: 'Security Scanner Unit 38',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200038',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20039',
  name: 'Navigation Equipment Unit 39',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200039',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20040',
  name: 'Traffic Control System Unit 40',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200040',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20041',
  name: 'Radar System Unit 41',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200041',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20042',
  name: 'Security Scanner Unit 42',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200042',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20043',
  name: 'Navigation Equipment Unit 43',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200043',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20044',
  name: 'Traffic Control System Unit 44',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200044',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20045',
  name: 'Radar System Unit 45',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200045',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MOUNTAIN", "GEO_STATE_CO", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20046',
  name: 'Security Scanner Unit 46',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200046',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MOUNTAIN", "GEO_STATE_CO", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20047',
  name: 'Navigation Equipment Unit 47',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200047',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MOUNTAIN", "GEO_STATE_CO", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20048',
  name: 'Traffic Control System Unit 48',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200048',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MOUNTAIN", "GEO_STATE_CO", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20049',
  name: 'Radar System Unit 49',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200049',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MOUNTAIN", "GEO_STATE_CO", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20050',
  name: 'Security Scanner Unit 50',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200050',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MOUNTAIN", "GEO_STATE_CO", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20051',
  name: 'Navigation Equipment Unit 51',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200051',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MOUNTAIN", "GEO_STATE_CO", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20052',
  name: 'Traffic Control System Unit 52',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200052',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MOUNTAIN", "GEO_STATE_CO", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20053',
  name: 'Radar System Unit 53',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200053',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20054',
  name: 'Security Scanner Unit 54',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200054',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20055',
  name: 'Navigation Equipment Unit 55',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200055',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20056',
  name: 'Traffic Control System Unit 56',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200056',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20057',
  name: 'Radar System Unit 57',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200057',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NJ", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20058',
  name: 'Security Scanner Unit 58',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200058',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NJ", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20059',
  name: 'Navigation Equipment Unit 59',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200059',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NJ", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20060',
  name: 'Traffic Control System Unit 60',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200060',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NJ", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20061',
  name: 'Radar System Unit 61',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200061',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_BRIDGE", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20062',
  name: 'Security Scanner Unit 62',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200062',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_BRIDGE", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20063',
  name: 'Navigation Equipment Unit 63',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200063',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_BRIDGE", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20064',
  name: 'Traffic Control System Unit 64',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200064',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_BRIDGE", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20065',
  name: 'Radar System Unit 65',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200065',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_BRIDGE", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20066',
  name: 'Security Scanner Unit 66',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200066',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_BRIDGE", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20067',
  name: 'Navigation Equipment Unit 67',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200067',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_BRIDGE", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20068',
  name: 'Traffic Control System Unit 68',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200068',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_BRIDGE", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20069',
  name: 'Radar System Unit 69',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200069',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_TUNNEL", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20070',
  name: 'Security Scanner Unit 70',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200070',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_TUNNEL", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20071',
  name: 'Navigation Equipment Unit 71',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200071',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_TUNNEL", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20072',
  name: 'Traffic Control System Unit 72',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200072',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_TUNNEL", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20073',
  name: 'Radar System Unit 73',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200073',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20074',
  name: 'Security Scanner Unit 74',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200074',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20075',
  name: 'Navigation Equipment Unit 75',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200075',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20076',
  name: 'Traffic Control System Unit 76',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200076',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20077',
  name: 'Radar System Unit 77',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200077',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20078',
  name: 'Security Scanner Unit 78',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200078',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20079',
  name: 'Navigation Equipment Unit 79',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200079',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20080',
  name: 'Traffic Control System Unit 80',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200080',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20081',
  name: 'Radar System Unit 81',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200081',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20082',
  name: 'Security Scanner Unit 82',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200082',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20083',
  name: 'Navigation Equipment Unit 83',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200083',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20084',
  name: 'Traffic Control System Unit 84',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200084',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TX", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20085',
  name: 'Radar System Unit 85',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200085',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20086',
  name: 'Security Scanner Unit 86',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200086',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20087',
  name: 'Navigation Equipment Unit 87',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200087',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20088',
  name: 'Traffic Control System Unit 88',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200088',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20089',
  name: 'Radar System Unit 89',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200089',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_MO", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20090',
  name: 'Security Scanner Unit 90',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200090',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_MO", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20091',
  name: 'Navigation Equipment Unit 91',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200091',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_MO", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20092',
  name: 'Traffic Control System Unit 92',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200092',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_MO", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20093',
  name: 'Radar System Unit 93',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200093',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20094',
  name: 'Security Scanner Unit 94',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200094',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20095',
  name: 'Navigation Equipment Unit 95',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200095',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20096',
  name: 'Traffic Control System Unit 96',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200096',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20097',
  name: 'Radar System Unit 97',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200097',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20098',
  name: 'Security Scanner Unit 98',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200098',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20099',
  name: 'Navigation Equipment Unit 99',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200099',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20100',
  name: 'Traffic Control System Unit 100',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200100',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20101',
  name: 'Radar System Unit 101',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200101',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20102',
  name: 'Security Scanner Unit 102',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200102',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20103',
  name: 'Navigation Equipment Unit 103',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200103',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20104',
  name: 'Traffic Control System Unit 104',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200104',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20105',
  name: 'Radar System Unit 105',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200105',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20106',
  name: 'Security Scanner Unit 106',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200106',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20107',
  name: 'Navigation Equipment Unit 107',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200107',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20108',
  name: 'Traffic Control System Unit 108',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200108',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20109',
  name: 'Radar System Unit 109',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200109',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20110',
  name: 'Security Scanner Unit 110',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200110',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20111',
  name: 'Navigation Equipment Unit 111',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200111',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20112',
  name: 'Traffic Control System Unit 112',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200112',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20113',
  name: 'Radar System Unit 113',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200113',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_TUNNEL", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20114',
  name: 'Security Scanner Unit 114',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200114',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_TUNNEL", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20115',
  name: 'Navigation Equipment Unit 115',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200115',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_TUNNEL", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20116',
  name: 'Traffic Control System Unit 116',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200116',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_TUNNEL", "OPS_FUNCTION_HIGHWAY", "REG_DOT_HIGHWAY_SAFETY", "REG_FHWA_STANDARDS", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20117',
  name: 'Radar System Unit 117',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200117',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_FL", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20118',
  name: 'Security Scanner Unit 118',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200118',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_FL", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20119',
  name: 'Navigation Equipment Unit 119',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200119',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_FL", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20120',
  name: 'Traffic Control System Unit 120',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200120',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_FL", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20121',
  name: 'Radar System Unit 121',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200121',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TN", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20122',
  name: 'Security Scanner Unit 122',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200122',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TN", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20123',
  name: 'Navigation Equipment Unit 123',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200123',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TN", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20124',
  name: 'Traffic Control System Unit 124',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200124',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_TN", "OPS_FACILITY_FREIGHT", "OPS_FUNCTION_CARGO", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20125',
  name: 'Radar System Unit 125',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200125',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_FL", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20126',
  name: 'Security Scanner Unit 126',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200126',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_FL", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20127',
  name: 'Navigation Equipment Unit 127',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200127',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_FL", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20128',
  name: 'Traffic Control System Unit 128',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200128',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_FL", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20129',
  name: 'Radar System Unit 129',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200129',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_FL", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20130',
  name: 'Security Scanner Unit 130',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200130',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_FL", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20131',
  name: 'Navigation Equipment Unit 131',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200131',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_FL", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20132',
  name: 'Traffic Control System Unit 132',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200132',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_FL", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20133',
  name: 'Radar System Unit 133',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200133',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_MN", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20134',
  name: 'Security Scanner Unit 134',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200134',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_MN", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20135',
  name: 'Navigation Equipment Unit 135',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200135',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_MN", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20136',
  name: 'Traffic Control System Unit 136',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200136',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_MN", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20137',
  name: 'Radar System Unit 137',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200137',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20138',
  name: 'Security Scanner Unit 138',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200138',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20139',
  name: 'Navigation Equipment Unit 139',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200139',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20140',
  name: 'Traffic Control System Unit 140',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200140',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20141',
  name: 'Radar System Unit 141',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200141',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20142',
  name: 'Security Scanner Unit 142',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200142',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20143',
  name: 'Navigation Equipment Unit 143',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200143',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20144',
  name: 'Traffic Control System Unit 144',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200144',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20145',
  name: 'Radar System Unit 145',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200145',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20146',
  name: 'Security Scanner Unit 146',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200146',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20147',
  name: 'Navigation Equipment Unit 147',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200147',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20148',
  name: 'Traffic Control System Unit 148',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200148',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_NY", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20149',
  name: 'Radar System Unit 149',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200149',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20150',
  name: 'Security Scanner Unit 150',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200150',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20151',
  name: 'Navigation Equipment Unit 151',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200151',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20152',
  name: 'Traffic Control System Unit 152',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200152',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20153',
  name: 'Radar System Unit 153',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200153',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20154',
  name: 'Security Scanner Unit 154',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200154',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20155',
  name: 'Navigation Equipment Unit 155',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200155',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20156',
  name: 'Traffic Control System Unit 156',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200156',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MIDWEST", "GEO_STATE_IL", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20157',
  name: 'Radar System Unit 157',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200157',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_PA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20158',
  name: 'Security Scanner Unit 158',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200158',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_PA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20159',
  name: 'Navigation Equipment Unit 159',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200159',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_PA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20160',
  name: 'Traffic Control System Unit 160',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200160',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_PA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20161',
  name: 'Radar System Unit 161',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200161',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MOUNTAIN", "GEO_STATE_AZ", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20162',
  name: 'Security Scanner Unit 162',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200162',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MOUNTAIN", "GEO_STATE_AZ", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20163',
  name: 'Navigation Equipment Unit 163',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200163',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MOUNTAIN", "GEO_STATE_AZ", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20164',
  name: 'Traffic Control System Unit 164',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200164',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_MOUNTAIN", "GEO_STATE_AZ", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20165',
  name: 'Radar System Unit 165',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200165',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_OR", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20166',
  name: 'Security Scanner Unit 166',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200166',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_OR", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20167',
  name: 'Navigation Equipment Unit 167',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200167',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_OR", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20168',
  name: 'Traffic Control System Unit 168',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200168',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_OR", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20169',
  name: 'Radar System Unit 169',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200169',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_GA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20170',
  name: 'Security Scanner Unit 170',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200170',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_GA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20171',
  name: 'Navigation Equipment Unit 171',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200171',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_GA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20172',
  name: 'Traffic Control System Unit 172',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200172',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_SOUTH", "GEO_STATE_GA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20173',
  name: 'Radar System Unit 173',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200173',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20174',
  name: 'Security Scanner Unit 174',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200174',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20175',
  name: 'Navigation Equipment Unit 175',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200175',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20176',
  name: 'Traffic Control System Unit 176',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200176',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20177',
  name: 'Radar System Unit 177',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200177',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20178',
  name: 'Security Scanner Unit 178',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200178',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20179',
  name: 'Navigation Equipment Unit 179',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200179',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20180',
  name: 'Traffic Control System Unit 180',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200180',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20181',
  name: 'Radar System Unit 181',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200181',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20182',
  name: 'Security Scanner Unit 182',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200182',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20183',
  name: 'Navigation Equipment Unit 183',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200183',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20184',
  name: 'Traffic Control System Unit 184',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200184',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20185',
  name: 'Radar System Unit 185',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200185',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20186',
  name: 'Security Scanner Unit 186',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200186',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20187',
  name: 'Navigation Equipment Unit 187',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200187',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20188',
  name: 'Traffic Control System Unit 188',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200188',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_CONTROL", "OPS_FUNCTION_TRAFFIC_MGMT", "REG_DOT_ITS", "REG_STATE_TRANSPORT", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20189',
  name: 'Radar System Unit 189',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200189',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20190',
  name: 'Security Scanner Unit 190',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200190',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20191',
  name: 'Navigation Equipment Unit 191',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200191',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20192',
  name: 'Traffic Control System Unit 192',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200192',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_WEST_COAST", "GEO_STATE_CA", "OPS_FACILITY_AIRPORT", "OPS_FUNCTION_AVIATION", "REG_TSA_AVIATION_SEC", "REG_FAA_AIRSPACE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20193',
  name: 'Radar System Unit 193',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200193',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20194',
  name: 'Security Scanner Unit 194',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200194',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20195',
  name: 'Navigation Equipment Unit 195',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200195',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20196',
  name: 'Traffic Control System Unit 196',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200196',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHWEST", "GEO_STATE_WA", "OPS_FACILITY_SEAPORT", "OPS_FUNCTION_MARITIME", "REG_USCG_MARITIME", "REG_MTSA_SECURITY", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20197',
  name: 'Radar System Unit 197',
  equipmentType: 'Radar System',
  manufacturer: 'Manufacturer-RadarSystem',
  model: 'Radar-System-2022',
  serial_number: 'SN-T-200197',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_DC", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_RADAR", "TECH_DETECTION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20198',
  name: 'Security Scanner Unit 198',
  equipmentType: 'Security Scanner',
  manufacturer: 'Manufacturer-SecurityScanner',
  model: 'Security-Scanner-2022',
  serial_number: 'SN-T-200198',
  installation_date: date('2022-01-01'),
  operational_status: 'maintenance',
  criticality_level: 'medium',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_DC", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_SCANNER", "TECH_SECURITY", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20199',
  name: 'Navigation Equipment Unit 199',
  equipmentType: 'Navigation Equipment',
  manufacturer: 'Manufacturer-NavigationEquipment',
  model: 'Navigation-Equipment-2022',
  serial_number: 'SN-T-200199',
  installation_date: date('2022-01-01'),
  operational_status: 'active',
  criticality_level: 'critical',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_DC", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_NAV", "TECH_GUIDANCE", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (eq:Equipment {
  equipmentId: 'EQ-TRANS-20200',
  name: 'Traffic Control System Unit 200',
  equipmentType: 'Traffic Control System',
  manufacturer: 'Manufacturer-TrafficControlSystem',
  model: 'Traffic-Control-System-2022',
  serial_number: 'SN-T-200200',
  installation_date: date('2022-01-01'),
  operational_status: 'standby',
  criticality_level: 'high',
  tags: ["TRANS_EQUIP", "SECTOR_TRANSPORTATION", "GEO_REGION_NORTHEAST", "GEO_STATE_DC", "OPS_FACILITY_RAILROAD", "OPS_FUNCTION_RAIL_PASSENGER", "REG_DOT_RAIL_SAFETY", "REG_FRA_COMPLIANCE", "TECH_EQUIP_CONTROL", "TECH_AUTOMATION", "TIME_ERA_CURRENT", "TIME_MAINT_PRIORITY_MEDIUM"],
  created_date: datetime(),
  updated_date: datetime()
});

// ═══════════════════════════════════════════════════════════════
// RELATIONSHIPS: LOCATED_AT (200 relationships)
// ═══════════════════════════════════════════════════════════════

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20001'}), (f:Facility {facilityId: 'TRANSPORT-ATL-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20002'}), (f:Facility {facilityId: 'TRANSPORT-ATL-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20003'}), (f:Facility {facilityId: 'TRANSPORT-ATL-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20004'}), (f:Facility {facilityId: 'TRANSPORT-ATL-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20005'}), (f:Facility {facilityId: 'TRANSPORT-ATL-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20006'}), (f:Facility {facilityId: 'TRANSPORT-ATL-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20007'}), (f:Facility {facilityId: 'TRANSPORT-ATL-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20008'}), (f:Facility {facilityId: 'TRANSPORT-ATL-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20009'}), (f:Facility {facilityId: 'TRANSPORT-BAL-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20010'}), (f:Facility {facilityId: 'TRANSPORT-BAL-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20011'}), (f:Facility {facilityId: 'TRANSPORT-BAL-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20012'}), (f:Facility {facilityId: 'TRANSPORT-BAL-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20013'}), (f:Facility {facilityId: 'TRANSPORT-BB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20014'}), (f:Facility {facilityId: 'TRANSPORT-BB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20015'}), (f:Facility {facilityId: 'TRANSPORT-BB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20016'}), (f:Facility {facilityId: 'TRANSPORT-BB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20017'}), (f:Facility {facilityId: 'TRANSPORT-BOS-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20018'}), (f:Facility {facilityId: 'TRANSPORT-BOS-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20019'}), (f:Facility {facilityId: 'TRANSPORT-BOS-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20020'}), (f:Facility {facilityId: 'TRANSPORT-BOS-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20021'}), (f:Facility {facilityId: 'TRANSPORT-BOS-SOUTH-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20022'}), (f:Facility {facilityId: 'TRANSPORT-BOS-SOUTH-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20023'}), (f:Facility {facilityId: 'TRANSPORT-BOS-SOUTH-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20024'}), (f:Facility {facilityId: 'TRANSPORT-BOS-SOUTH-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20025'}), (f:Facility {facilityId: 'TRANSPORT-CHA-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20026'}), (f:Facility {facilityId: 'TRANSPORT-CHA-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20027'}), (f:Facility {facilityId: 'TRANSPORT-CHA-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20028'}), (f:Facility {facilityId: 'TRANSPORT-CHA-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20029'}), (f:Facility {facilityId: 'TRANSPORT-CHI-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20030'}), (f:Facility {facilityId: 'TRANSPORT-CHI-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20031'}), (f:Facility {facilityId: 'TRANSPORT-CHI-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20032'}), (f:Facility {facilityId: 'TRANSPORT-CHI-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20033'}), (f:Facility {facilityId: 'TRANSPORT-CHI-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20034'}), (f:Facility {facilityId: 'TRANSPORT-CHI-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20035'}), (f:Facility {facilityId: 'TRANSPORT-CHI-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20036'}), (f:Facility {facilityId: 'TRANSPORT-CHI-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20037'}), (f:Facility {facilityId: 'TRANSPORT-CHI-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20038'}), (f:Facility {facilityId: 'TRANSPORT-CHI-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20039'}), (f:Facility {facilityId: 'TRANSPORT-CHI-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20040'}), (f:Facility {facilityId: 'TRANSPORT-CHI-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20041'}), (f:Facility {facilityId: 'TRANSPORT-DAL-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20042'}), (f:Facility {facilityId: 'TRANSPORT-DAL-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20043'}), (f:Facility {facilityId: 'TRANSPORT-DAL-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20044'}), (f:Facility {facilityId: 'TRANSPORT-DAL-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20045'}), (f:Facility {facilityId: 'TRANSPORT-DEN-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20046'}), (f:Facility {facilityId: 'TRANSPORT-DEN-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20047'}), (f:Facility {facilityId: 'TRANSPORT-DEN-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20048'}), (f:Facility {facilityId: 'TRANSPORT-DEN-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20049'}), (f:Facility {facilityId: 'TRANSPORT-DEN-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20050'}), (f:Facility {facilityId: 'TRANSPORT-DEN-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20051'}), (f:Facility {facilityId: 'TRANSPORT-DEN-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20052'}), (f:Facility {facilityId: 'TRANSPORT-DEN-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20053'}), (f:Facility {facilityId: 'TRANSPORT-DFW-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20054'}), (f:Facility {facilityId: 'TRANSPORT-DFW-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20055'}), (f:Facility {facilityId: 'TRANSPORT-DFW-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20056'}), (f:Facility {facilityId: 'TRANSPORT-DFW-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20057'}), (f:Facility {facilityId: 'TRANSPORT-EWR-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20058'}), (f:Facility {facilityId: 'TRANSPORT-EWR-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20059'}), (f:Facility {facilityId: 'TRANSPORT-EWR-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20060'}), (f:Facility {facilityId: 'TRANSPORT-EWR-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20061'}), (f:Facility {facilityId: 'TRANSPORT-GB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20062'}), (f:Facility {facilityId: 'TRANSPORT-GB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20063'}), (f:Facility {facilityId: 'TRANSPORT-GB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20064'}), (f:Facility {facilityId: 'TRANSPORT-GB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20065'}), (f:Facility {facilityId: 'TRANSPORT-GWB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20066'}), (f:Facility {facilityId: 'TRANSPORT-GWB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20067'}), (f:Facility {facilityId: 'TRANSPORT-GWB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20068'}), (f:Facility {facilityId: 'TRANSPORT-GWB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20069'}), (f:Facility {facilityId: 'TRANSPORT-HOL-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20070'}), (f:Facility {facilityId: 'TRANSPORT-HOL-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20071'}), (f:Facility {facilityId: 'TRANSPORT-HOL-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20072'}), (f:Facility {facilityId: 'TRANSPORT-HOL-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20073'}), (f:Facility {facilityId: 'TRANSPORT-HOU-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20074'}), (f:Facility {facilityId: 'TRANSPORT-HOU-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20075'}), (f:Facility {facilityId: 'TRANSPORT-HOU-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20076'}), (f:Facility {facilityId: 'TRANSPORT-HOU-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20077'}), (f:Facility {facilityId: 'TRANSPORT-HOU-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20078'}), (f:Facility {facilityId: 'TRANSPORT-HOU-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20079'}), (f:Facility {facilityId: 'TRANSPORT-HOU-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20080'}), (f:Facility {facilityId: 'TRANSPORT-HOU-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20081'}), (f:Facility {facilityId: 'TRANSPORT-IAH-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20082'}), (f:Facility {facilityId: 'TRANSPORT-IAH-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20083'}), (f:Facility {facilityId: 'TRANSPORT-IAH-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20084'}), (f:Facility {facilityId: 'TRANSPORT-IAH-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20085'}), (f:Facility {facilityId: 'TRANSPORT-JFK-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20086'}), (f:Facility {facilityId: 'TRANSPORT-JFK-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20087'}), (f:Facility {facilityId: 'TRANSPORT-JFK-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20088'}), (f:Facility {facilityId: 'TRANSPORT-JFK-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20089'}), (f:Facility {facilityId: 'TRANSPORT-KC-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20090'}), (f:Facility {facilityId: 'TRANSPORT-KC-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20091'}), (f:Facility {facilityId: 'TRANSPORT-KC-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20092'}), (f:Facility {facilityId: 'TRANSPORT-KC-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20093'}), (f:Facility {facilityId: 'TRANSPORT-LA-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20094'}), (f:Facility {facilityId: 'TRANSPORT-LA-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20095'}), (f:Facility {facilityId: 'TRANSPORT-LA-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20096'}), (f:Facility {facilityId: 'TRANSPORT-LA-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20097'}), (f:Facility {facilityId: 'TRANSPORT-LA-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20098'}), (f:Facility {facilityId: 'TRANSPORT-LA-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20099'}), (f:Facility {facilityId: 'TRANSPORT-LA-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20100'}), (f:Facility {facilityId: 'TRANSPORT-LA-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20101'}), (f:Facility {facilityId: 'TRANSPORT-LALB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20102'}), (f:Facility {facilityId: 'TRANSPORT-LALB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20103'}), (f:Facility {facilityId: 'TRANSPORT-LALB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20104'}), (f:Facility {facilityId: 'TRANSPORT-LALB-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20105'}), (f:Facility {facilityId: 'TRANSPORT-LAX-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20106'}), (f:Facility {facilityId: 'TRANSPORT-LAX-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20107'}), (f:Facility {facilityId: 'TRANSPORT-LAX-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20108'}), (f:Facility {facilityId: 'TRANSPORT-LAX-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20109'}), (f:Facility {facilityId: 'TRANSPORT-LAX-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20110'}), (f:Facility {facilityId: 'TRANSPORT-LAX-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20111'}), (f:Facility {facilityId: 'TRANSPORT-LAX-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20112'}), (f:Facility {facilityId: 'TRANSPORT-LAX-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20113'}), (f:Facility {facilityId: 'TRANSPORT-LC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20114'}), (f:Facility {facilityId: 'TRANSPORT-LC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20115'}), (f:Facility {facilityId: 'TRANSPORT-LC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20116'}), (f:Facility {facilityId: 'TRANSPORT-LC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20117'}), (f:Facility {facilityId: 'TRANSPORT-MCO-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20118'}), (f:Facility {facilityId: 'TRANSPORT-MCO-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20119'}), (f:Facility {facilityId: 'TRANSPORT-MCO-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20120'}), (f:Facility {facilityId: 'TRANSPORT-MCO-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20121'}), (f:Facility {facilityId: 'TRANSPORT-MEM-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20122'}), (f:Facility {facilityId: 'TRANSPORT-MEM-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20123'}), (f:Facility {facilityId: 'TRANSPORT-MEM-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20124'}), (f:Facility {facilityId: 'TRANSPORT-MEM-FREIGHT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20125'}), (f:Facility {facilityId: 'TRANSPORT-MIA-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20126'}), (f:Facility {facilityId: 'TRANSPORT-MIA-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20127'}), (f:Facility {facilityId: 'TRANSPORT-MIA-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20128'}), (f:Facility {facilityId: 'TRANSPORT-MIA-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20129'}), (f:Facility {facilityId: 'TRANSPORT-MIA-PORT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20130'}), (f:Facility {facilityId: 'TRANSPORT-MIA-PORT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20131'}), (f:Facility {facilityId: 'TRANSPORT-MIA-PORT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20132'}), (f:Facility {facilityId: 'TRANSPORT-MIA-PORT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20133'}), (f:Facility {facilityId: 'TRANSPORT-MSP-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20134'}), (f:Facility {facilityId: 'TRANSPORT-MSP-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20135'}), (f:Facility {facilityId: 'TRANSPORT-MSP-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20136'}), (f:Facility {facilityId: 'TRANSPORT-MSP-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20137'}), (f:Facility {facilityId: 'TRANSPORT-NY-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20138'}), (f:Facility {facilityId: 'TRANSPORT-NY-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20139'}), (f:Facility {facilityId: 'TRANSPORT-NY-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20140'}), (f:Facility {facilityId: 'TRANSPORT-NY-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20141'}), (f:Facility {facilityId: 'TRANSPORT-NYC-PENN-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20142'}), (f:Facility {facilityId: 'TRANSPORT-NYC-PENN-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20143'}), (f:Facility {facilityId: 'TRANSPORT-NYC-PENN-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20144'}), (f:Facility {facilityId: 'TRANSPORT-NYC-PENN-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20145'}), (f:Facility {facilityId: 'TRANSPORT-NYNJ-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20146'}), (f:Facility {facilityId: 'TRANSPORT-NYNJ-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20147'}), (f:Facility {facilityId: 'TRANSPORT-NYNJ-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20148'}), (f:Facility {facilityId: 'TRANSPORT-NYNJ-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20149'}), (f:Facility {facilityId: 'TRANSPORT-OAK-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20150'}), (f:Facility {facilityId: 'TRANSPORT-OAK-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20151'}), (f:Facility {facilityId: 'TRANSPORT-OAK-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20152'}), (f:Facility {facilityId: 'TRANSPORT-OAK-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20153'}), (f:Facility {facilityId: 'TRANSPORT-ORD-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20154'}), (f:Facility {facilityId: 'TRANSPORT-ORD-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20155'}), (f:Facility {facilityId: 'TRANSPORT-ORD-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20156'}), (f:Facility {facilityId: 'TRANSPORT-ORD-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20157'}), (f:Facility {facilityId: 'TRANSPORT-PHIL-30TH-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20158'}), (f:Facility {facilityId: 'TRANSPORT-PHIL-30TH-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20159'}), (f:Facility {facilityId: 'TRANSPORT-PHIL-30TH-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20160'}), (f:Facility {facilityId: 'TRANSPORT-PHIL-30TH-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20161'}), (f:Facility {facilityId: 'TRANSPORT-PHX-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20162'}), (f:Facility {facilityId: 'TRANSPORT-PHX-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20163'}), (f:Facility {facilityId: 'TRANSPORT-PHX-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20164'}), (f:Facility {facilityId: 'TRANSPORT-PHX-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20165'}), (f:Facility {facilityId: 'TRANSPORT-PORT-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20166'}), (f:Facility {facilityId: 'TRANSPORT-PORT-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20167'}), (f:Facility {facilityId: 'TRANSPORT-PORT-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20168'}), (f:Facility {facilityId: 'TRANSPORT-PORT-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20169'}), (f:Facility {facilityId: 'TRANSPORT-SAV-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20170'}), (f:Facility {facilityId: 'TRANSPORT-SAV-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20171'}), (f:Facility {facilityId: 'TRANSPORT-SAV-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20172'}), (f:Facility {facilityId: 'TRANSPORT-SAV-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20173'}), (f:Facility {facilityId: 'TRANSPORT-SEA-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20174'}), (f:Facility {facilityId: 'TRANSPORT-SEA-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20175'}), (f:Facility {facilityId: 'TRANSPORT-SEA-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20176'}), (f:Facility {facilityId: 'TRANSPORT-SEA-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20177'}), (f:Facility {facilityId: 'TRANSPORT-SEA-KING-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20178'}), (f:Facility {facilityId: 'TRANSPORT-SEA-KING-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20179'}), (f:Facility {facilityId: 'TRANSPORT-SEA-KING-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20180'}), (f:Facility {facilityId: 'TRANSPORT-SEA-KING-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20181'}), (f:Facility {facilityId: 'TRANSPORT-SEA-PORT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20182'}), (f:Facility {facilityId: 'TRANSPORT-SEA-PORT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20183'}), (f:Facility {facilityId: 'TRANSPORT-SEA-PORT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20184'}), (f:Facility {facilityId: 'TRANSPORT-SEA-PORT-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20185'}), (f:Facility {facilityId: 'TRANSPORT-SF-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20186'}), (f:Facility {facilityId: 'TRANSPORT-SF-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20187'}), (f:Facility {facilityId: 'TRANSPORT-SF-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20188'}), (f:Facility {facilityId: 'TRANSPORT-SF-TMC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20189'}), (f:Facility {facilityId: 'TRANSPORT-SFO-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20190'}), (f:Facility {facilityId: 'TRANSPORT-SFO-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20191'}), (f:Facility {facilityId: 'TRANSPORT-SFO-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20192'}), (f:Facility {facilityId: 'TRANSPORT-SFO-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20193'}), (f:Facility {facilityId: 'TRANSPORT-TAC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20194'}), (f:Facility {facilityId: 'TRANSPORT-TAC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20195'}), (f:Facility {facilityId: 'TRANSPORT-TAC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20196'}), (f:Facility {facilityId: 'TRANSPORT-TAC-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20197'}), (f:Facility {facilityId: 'TRANSPORT-WASH-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 1',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20198'}), (f:Facility {facilityId: 'TRANSPORT-WASH-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 2',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20199'}), (f:Facility {facilityId: 'TRANSPORT-WASH-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 3',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

MATCH (eq:Equipment {equipmentId: 'EQ-TRANS-20200'}), (f:Facility {facilityId: 'TRANSPORT-WASH-UNION-001'})
CREATE (eq)-[:LOCATED_AT {
  installation_date: date('2022-01-01'),
  location: 'Zone 4',
  exact_coordinates: point({latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005})
}]->(f);

// ═══════════════════════════════════════════════════════════════
// VERIFICATION QUERIES
// ═══════════════════════════════════════════════════════════════

// Count equipment
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-TRANS-'
RETURN COUNT(eq) AS equipment_count;

// Count relationships
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-TRANS-'
RETURN COUNT(r) AS relationship_count,
       COUNT(DISTINCT eq) AS unique_equipment,
       COUNT(DISTINCT f) AS unique_facilities;

// Tag statistics
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-TRANS-'
WITH eq, size(eq.tags) AS tag_count
RETURN AVG(tag_count) AS avg_tags,
       MIN(tag_count) AS min_tags,
       MAX(tag_count) AS max_tags;

// ═══════════════════════════════════════════════════════════════
// END OF TRANSPORTATION SECTOR DEPLOYMENT
// ═══════════════════════════════════════════════════════════════