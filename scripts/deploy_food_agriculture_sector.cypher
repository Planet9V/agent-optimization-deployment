// Food & Agriculture Sector - TASKMASTER Task 12
// Target: 700 equipment, 90 facilities

// Food Processing Plants (25 facilities, 250 equipment)
CREATE (f1:Facility {facilityId: "FOOD-PROC-IA-001", name: "Iowa Meat Processing Plant", facilityType: "FOOD_PROCESSING_PLANT", sector: "FOOD_AGRICULTURE", latitude: 41.5868, longitude: -93.6250, state: "IA"})
UNWIND range(1, 10) as i CREATE (e:Equipment {equipmentId: "EQ-FOOD-PROC-IA-001-" + i, equipmentType: CASE i WHEN 1 THEN "PLC" WHEN 2 THEN "SCADA System" WHEN 3 THEN "Temperature Monitor" WHEN 4 THEN "Conveyor Control" WHEN 5 THEN "Refrigeration System" WHEN 6 THEN "Router" ELSE "Quality Control System" END, tags: ["SECTOR_FOOD_AGRICULTURE", "SUBSECTOR_FOOD_PROCESSING", "REG_FDA", "REG_USDA_FSIS"] + CASE i WHEN 1 THEN ["SECTOR_INDUSTRIAL_CONTROL", "ICS_PLC"] WHEN 2 THEN ["SECTOR_INDUSTRIAL_CONTROL", "ICS_SCADA"] WHEN 6 THEN ["SECTOR_COMMON_IT"] ELSE [] END})-[:LOCATED_AT]->(f1);

// Farms with IoT (40 facilities, 280 equipment)
// Grain Elevators (15 facilities, 105 equipment)
// Cold Storage (10 facilities, 65 equipment)

// VALIDATION: Expected 700 equipment
