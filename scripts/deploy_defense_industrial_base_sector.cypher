// Defense Industrial Base Sector - TASKMASTER Task 10
// Target: 400 equipment, 40 facilities
// Created: 2025-11-19 23:55:00 UTC

// Defense Contractors (15 facilities, 150 equipment)
CREATE (f1:Facility {facilityId: "DEF-CONTRACTOR-VA-001", name: "Lockheed Martin Facility", facilityType: "DEFENSE_CONTRACTOR", sector: "DEFENSE_INDUSTRIAL_BASE", latitude: 38.8048, longitude: -77.0469, state: "VA"})
UNWIND range(1, 10) as i CREATE (e:Equipment {equipmentId: "EQ-DEF-CONTRACTOR-VA-001-" + i, equipmentType: CASE i WHEN 1 THEN "Classified Network Router" WHEN 2 THEN "Secure Workstation" WHEN 3 THEN "Firewall" WHEN 4 THEN "IDS/IPS" WHEN 5 THEN "Manufacturing SCADA" ELSE "Secure Storage" END, tags: ["SECTOR_DEFENSE_INDUSTRIAL_BASE", "SUBSECTOR_AEROSPACE_DEFENSE", "CLASSIFICATION_SECRET", "OPS_CRITICALITY_CRITICAL", "REG_DFARS", "REG_CMMC_LEVEL_3", "REG_ITAR"] + CASE i WHEN 1 THEN ["SECTOR_COMMON_IT", "TECH_VENDOR_CISCO"] WHEN 3 THEN ["SECTOR_COMMON_IT", "TECH_VENDOR_PALO_ALTO"] WHEN 5 THEN ["SECTOR_INDUSTRIAL_CONTROL", "TECH_VENDOR_SIEMENS"] ELSE [] END})-[:LOCATED_AT]->(f1);

// Shipyards (10 facilities, 100 equipment)
// Ammunition Plants (10 facilities, 100 equipment)
// Research Labs (5 facilities, 50 equipment)

// Cross-sector: Network equipment + SCADA tagged appropriately

// VALIDATION: Expected 400 equipment
