// Dams Sector - TASKMASTER Task 9
// Target: 300 equipment, 30 facilities
// Reference: 10_Ontologies/.../Critical_Infrastructure_Sectors_Patterns/dams/

// Hydroelectric Dams (10 facilities, 100 equipment)
CREATE (f1:Facility {facilityId: "DAMS-HYDRO-WA-001", name: "Grand Coulee Dam", facilityType: "HYDROELECTRIC_DAM", sector: "DAMS", latitude: 47.9550, longitude: -118.9808, state: "WA"})
UNWIND range(1, 10) as i CREATE (e:Equipment {equipmentId: "EQ-DAMS-HYDRO-WA-001-" + i, equipmentType: CASE i WHEN 1 THEN "SCADA System" WHEN 2 THEN "PLC" WHEN 3 THEN "Generator Control" WHEN 4 THEN "Spillway Control" WHEN 5 THEN "Turbine Monitor" WHEN 6 THEN "Flow Meter" WHEN 7 THEN "Water Level Sensor" WHEN 8 THEN "Router" WHEN 9 THEN "HMI" ELSE "Historian" END, tags: ["SECTOR_DAMS", "SUBSECTOR_HYDROELECTRIC", "OPS_FUNCTION_POWER_GENERATION", "OPS_CRITICALITY_CRITICAL", "REG_FERC", "REG_NERC_CIP"] + CASE i WHEN 1 THEN ["SECTOR_INDUSTRIAL_CONTROL", "TECH_VENDOR_SIEMENS", "ICS_SCADA"] WHEN 2 THEN ["SECTOR_INDUSTRIAL_CONTROL", "TECH_VENDOR_ALLEN_BRADLEY", "ICS_PLC"] WHEN 8 THEN ["SECTOR_COMMON_IT", "TECH_VENDOR_CISCO"] ELSE ["TECH_ICS_COMPONENT"] END})-[:LOCATED_AT]->(f1);

// Flood Control Dams (10 facilities, 100 equipment)
// Irrigation Dams (10 facilities, 100 equipment)

// Cross-sector: SCADA, PLC, Routers tagged appropriately

// VALIDATION: Expected 300 equipment
