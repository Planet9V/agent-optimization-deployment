// Nuclear Reactors, Materials & Waste Sector - TASKMASTER Task 13
// Target: 200 equipment, 20 facilities

// Nuclear Power Plants (10 facilities, 100 equipment)
CREATE (f1:Facility {facilityId: "NUC-POWER-PA-001", name: "Three Mile Island Nuclear", facilityType: "NUCLEAR_POWER_PLANT", sector: "NUCLEAR", latitude: 40.1531, longitude: -76.7250, state: "PA"})
UNWIND range(1, 10) as i CREATE (e:Equipment {equipmentId: "EQ-NUC-POWER-PA-001-" + i, equipmentType: CASE i WHEN 1 THEN "Reactor Control System" WHEN 2 THEN "Safety System PLC" WHEN 3 THEN "Radiation Monitor" WHEN 4 THEN "Emergency Shutdown" WHEN 5 THEN "Turbine Control" WHEN 6 THEN "Router" ELSE "SCADA System" END, tags: ["SECTOR_NUCLEAR", "SUBSECTOR_NUCLEAR_POWER", "CLASSIFICATION_HIGH_SECURITY", "OPS_CRITICALITY_CRITICAL", "REG_NRC", "REG_NERC_CIP"] + CASE i WHEN 1 THEN ["SECTOR_INDUSTRIAL_CONTROL", "SAFETY_CRITICAL"] WHEN 2 THEN ["SECTOR_INDUSTRIAL_CONTROL", "SAFETY_CRITICAL"] WHEN 6 THEN ["SECTOR_COMMON_IT"] WHEN 7 THEN ["SECTOR_INDUSTRIAL_CONTROL", "ICS_SCADA"] ELSE [] END})-[:LOCATED_AT]->(f1);

// Nuclear Waste Facilities (5 facilities, 50 equipment)
// Materials Research Labs (5 facilities, 50 equipment)

// Cross-sector: Industrial control + network equipment

// VALIDATION: Expected 200 equipment
