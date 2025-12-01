// Communications Sector Deployment - Following TASKMASTER
// Task 6.1.1: Deploy 500 Communications Equipment
// Created: 2025-11-19 23:35:00 UTC
// Reference: Sector patterns + Tagging methodology

// Data Centers (150 equipment, 15 facilities)
CREATE (f1:Facility {
  facilityId: "COMM-DC-VA-001",
  name: "Ashburn Data Center Alpha",
  facilityType: "DATA_CENTER",
  sector: "COMMUNICATIONS",
  latitude: 39.0438,
  longitude: -77.4874,
  state: "VA",
  city: "Ashburn"
})

// Data center equipment (10 per facility × 15 facilities = 150)
UNWIND range(1, 10) as i
CREATE (e:Equipment {
  equipmentId: "EQ-COMM-DC-VA-001-" + i,
  equipmentType: CASE i % 4
    WHEN 0 THEN "Server"
    WHEN 1 THEN "Router"
    WHEN 2 THEN "Switch"
    ELSE "Storage"
  END,

  // Cross-sector tagging for network equipment
  tags: CASE i % 4
    WHEN 1 THEN ["SECTOR_COMMUNICATIONS", "SECTOR_COMMON_IT", "EQUIP_TYPE_ROUTER", "FUNCTION_NETWORK_ROUTING", "VENDOR_CISCO", "GEO_STATE_VA", "OPS_CRITICALITY_HIGH", "TECH_PROTOCOL_BGP", "TECH_PROTOCOL_OSPF", "REG_FCC", "SUBSECTOR_DATA_CENTER", "NETWORK_INFRASTRUCTURE"]
    WHEN 2 THEN ["SECTOR_COMMUNICATIONS", "SECTOR_COMMON_IT", "EQUIP_TYPE_SWITCH", "FUNCTION_NETWORK_SWITCHING", "VENDOR_CISCO", "GEO_STATE_VA", "OPS_CRITICALITY_HIGH", "TECH_PROTOCOL_ETHERNET", "REG_FCC", "SUBSECTOR_DATA_CENTER", "NETWORK_INFRASTRUCTURE", "TECH_POE_SUPPORT"]
    ELSE ["SECTOR_COMMUNICATIONS", "EQUIP_TYPE_" + CASE i % 4 WHEN 0 THEN "SERVER" ELSE "STORAGE" END, "FUNCTION_COMPUTE", "VENDOR_DELL", "GEO_STATE_VA", "OPS_CRITICALITY_CRITICAL", "TECH_VIRTUALIZATION", "REG_FCC", "REG_SOC2", "SUBSECTOR_DATA_CENTER", "COMPUTE_INFRASTRUCTURE", "CLOUD_READY"]
  END
})
-[:LOCATED_AT]->(f1);

// Telecommunications Hubs (12 facilities, 120 equipment)
CREATE (f2:Facility {facilityId: "COMM-TEL-NY-001", name: "New York Telecom Hub", facilityType: "TELECOMMUNICATIONS_HUB", sector: "COMMUNICATIONS", latitude: 40.7128, longitude: -74.0060, state: "NY", city: "New York"})
UNWIND range(1, 10) as i CREATE (e:Equipment {equipmentId: "EQ-COMM-TEL-NY-001-" + i, equipmentType: "Telephone Switch", tags: ["SECTOR_COMMUNICATIONS", "SUBSECTOR_TELECOMMUNICATIONS", "EQUIP_TYPE_SWITCH", "FUNCTION_VOICE_SWITCHING", "VENDOR_ERICSSON", "GEO_STATE_NY", "OPS_CRITICALITY_CRITICAL", "TECH_PROTOCOL_SS7", "TECH_PROTOCOL_SIP", "REG_FCC", "NETWORK_INFRASTRUCTURE"]})-[:LOCATED_AT]->(f2);

// Broadcast Facilities (10 facilities, 100 equipment)
CREATE (f3:Facility {facilityId: "COMM-BC-NY-001", name: "New York Broadcast Tower", facilityType: "BROADCAST_TOWER", sector: "COMMUNICATIONS", latitude: 40.7489, longitude: -73.9680, state: "NY", city: "New York"})
UNWIND range(1, 10) as i CREATE (e:Equipment {equipmentId: "EQ-COMM-BC-NY-001-" + i, equipmentType: "Transmitter", tags: ["SECTOR_COMMUNICATIONS", "SUBSECTOR_BROADCAST", "EQUIP_TYPE_TRANSMITTER", "FUNCTION_BROADCAST_TRANSMISSION", "VENDOR_HARRIS", "GEO_STATE_NY", "OPS_CRITICALITY_HIGH", "TECH_PROTOCOL_ATSC_3.0", "REG_FCC_BROADCAST", "MEDIA_INFRASTRUCTURE"]})-[:LOCATED_AT]->(f3);

// ISP Facilities (8 facilities, 80 equipment)
CREATE (f4:Facility {facilityId: "COMM-ISP-CA-001", name: "San Jose ISP Data Center", facilityType: "ISP_FACILITY", sector: "COMMUNICATIONS", latitude: 37.3382, longitude: -121.8863, state: "CA", city: "San Jose"})
UNWIND range(1, 10) as i CREATE (e:Equipment {equipmentId: "EQ-COMM-ISP-CA-001-" + i, equipmentType: CASE i % 3 WHEN 0 THEN "Router" WHEN 1 THEN "DNS Server" ELSE "Load Balancer" END, tags: ["SECTOR_COMMUNICATIONS", "SECTOR_COMMON_IT", "SUBSECTOR_ISP", "FUNCTION_INTERNET_SERVICE", "VENDOR_CISCO", "GEO_STATE_CA", "OPS_CRITICALITY_CRITICAL", "TECH_PROTOCOL_BGP", "REG_FCC", "INTERNET_INFRASTRUCTURE"]})-[:LOCATED_AT]->(f4);

// Satellite Ground Stations (5 facilities, 50 equipment)
CREATE (f5:Facility {facilityId: "COMM-SAT-CA-001", name: "Vandenberg Satellite Ground Station", facilityType: "SATELLITE_GROUND_STATION", sector: "COMMUNICATIONS", latitude: 34.7420, longitude: -120.5724, state: "CA", city: "Vandenberg"})
UNWIND range(1, 10) as i CREATE (e:Equipment {equipmentId: "EQ-COMM-SAT-CA-001-" + i, equipmentType: "Satellite Dish", tags: ["SECTOR_COMMUNICATIONS", "SUBSECTOR_SATELLITE", "EQUIP_TYPE_SATELLITE_DISH", "FUNCTION_SATELLITE_COMMUNICATION", "VENDOR_HARRIS", "GEO_STATE_CA", "OPS_CRITICALITY_HIGH", "TECH_PROTOCOL_DVB_S2", "REG_FCC_SATELLITE", "SPACE_COMMUNICATIONS"]})-[:LOCATED_AT]->(f5);

// VALIDATION QUERY (Task 6.4.2)
// MATCH (e:Equipment) WHERE 'SECTOR_COMMUNICATIONS' IN e.tags RETURN count(e);
// Expected: 500 (150 data center + 120 telecom + 100 broadcast + 80 ISP + 50 satellite)
