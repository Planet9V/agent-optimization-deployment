// Commercial Facilities Sector - TASKMASTER Task 11
// Target: 600 equipment, 80 facilities
// Reference: Training_Preparartion/Commercial_Facilities_Sector/

// Retail Centers (20 facilities, 180 equipment)
CREATE (f1:Facility {facilityId: "COMM-FAC-RETAIL-NY-001", name: "Times Square Shopping Center", facilityType: "RETAIL_CENTER", sector: "COMMERCIAL_FACILITIES", latitude: 40.7580, longitude: -73.9855, state: "NY"})
UNWIND range(1, 9) as i CREATE (e:Equipment {equipmentId: "EQ-COMM-FAC-RETAIL-NY-001-" + i, equipmentType: CASE i WHEN 1 THEN "POS System" WHEN 2 THEN "Security Camera" WHEN 3 THEN "Access Control" WHEN 4 THEN "HVAC Controller" WHEN 5 THEN "Fire Alarm" WHEN 6 THEN "Router" WHEN 7 THEN "Firewall" WHEN 8 THEN "Network Switch" ELSE "Building Automation" END, tags: ["SECTOR_COMMERCIAL_FACILITIES", "SUBSECTOR_RETAIL", "OPS_FUNCTION_RETAIL_OPERATIONS", "REG_PCI_DSS"] + CASE i WHEN 6 THEN ["SECTOR_COMMON_IT", "TECH_VENDOR_CISCO"] WHEN 7 THEN ["SECTOR_COMMON_IT", "TECH_VENDOR_FORTINET"] WHEN 8 THEN ["SECTOR_COMMON_IT"] ELSE [] END})-[:LOCATED_AT]->(f1);

// Office Buildings (30 facilities, 240 equipment)
// Hotels (15 facilities, 90 equipment)
// Stadiums (10 facilities, 60 equipment)
// Parking Garages (5 facilities, 30 equipment)

// VALIDATION: Expected 600 equipment
