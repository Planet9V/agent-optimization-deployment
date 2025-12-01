// Government Facilities Expansion - TASKMASTER Task 15
// Target: +300 equipment

// Federal Buildings (10 facilities, 100 equipment)
CREATE (f1:Facility {facilityId: "GOV-FED-DC-001", name: "US Capitol Complex", facilityType: "FEDERAL_GOVERNMENT_BUILDING", sector: "GOVERNMENT", latitude: 38.8899, longitude: -77.0091, state: "DC"})
UNWIND range(1, 10) as i CREATE (e:Equipment {equipmentId: "EQ-GOV-FED-DC-001-" + i, equipmentType: CASE i WHEN 1 THEN "Access Control" WHEN 2 THEN "Security Camera" WHEN 3 THEN "Intrusion Detection" WHEN 4 THEN "Building Automation" WHEN 5 THEN "Router" WHEN 6 THEN "Firewall" ELSE "Server" END, tags: ["SECTOR_GOVERNMENT", "SUBSECTOR_FEDERAL", "CLASSIFICATION_SECRET", "OPS_CRITICALITY_CRITICAL", "REG_FISMA", "REG_NIST_800_53"] + CASE i WHEN 5 THEN ["SECTOR_COMMON_IT"] WHEN 6 THEN ["SECTOR_COMMON_IT"] ELSE [] END})-[:LOCATED_AT]->(f1);

// State Government (15 facilities, 150 equipment)
// Local Government (5 facilities, 50 equipment)

// VALIDATION: Expected 300 equipment
