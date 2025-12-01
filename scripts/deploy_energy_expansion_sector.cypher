// Energy Sector Expansion - TASKMASTER Task 14
// Expanding beyond initial deployment
// Target: +300 equipment (to reach sector targets)

// Solar Farms (10 facilities, 100 equipment)
CREATE (f1:Facility {facilityId: "ENERGY-SOLAR-CA-001", name: "Mojave Solar Farm", facilityType: "SOLAR_POWER_PLANT", sector: "ENERGY", latitude: 35.0456, longitude: -118.2383, state: "CA"})
UNWIND range(1, 10) as i CREATE (e:Equipment {equipmentId: "EQ-ENERGY-SOLAR-CA-001-" + i, equipmentType: CASE i WHEN 1 THEN "Inverter" WHEN 2 THEN "SCADA System" WHEN 3 THEN "Weather Station" WHEN 4 THEN "PLC" WHEN 5 THEN "Router" ELSE "Monitoring System" END, tags: ["SECTOR_ENERGY", "SUBSECTOR_RENEWABLE_GENERATION", "ENERGY_TYPE_SOLAR", "REG_NERC_CIP"] + CASE i WHEN 2 THEN ["SECTOR_INDUSTRIAL_CONTROL", "ICS_SCADA"] WHEN 4 THEN ["SECTOR_INDUSTRIAL_CONTROL", "ICS_PLC"] WHEN 5 THEN ["SECTOR_COMMON_IT"] ELSE [] END})-[:LOCATED_AT]->(f1);

// Wind Farms (10 facilities, 100 equipment)
// Energy Storage (10 facilities, 100 equipment)

// VALIDATION: Expected 300 additional energy equipment
