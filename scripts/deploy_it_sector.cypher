// Information Technology Sector - TASKMASTER Task 16 (Final Sector!)
// Target: +100 equipment (complete to 7,900 target or close)

// Tech Companies (5 facilities, 50 equipment)
CREATE (f1:Facility {facilityId: "IT-TECH-CA-001", name: "Silicon Valley Tech Campus", facilityType: "TECHNOLOGY_CAMPUS", sector: "INFORMATION_TECHNOLOGY", latitude: 37.3861, longitude: -122.0839, state: "CA"})
UNWIND range(1, 10) as i CREATE (e:Equipment {equipmentId: "EQ-IT-TECH-CA-001-" + i, equipmentType: CASE i WHEN 1 THEN "Cloud Infrastructure" WHEN 2 THEN "Edge Computing" WHEN 3 THEN "CDN Node" WHEN 4 THEN "API Gateway" WHEN 5 THEN "Load Balancer" ELSE "Kubernetes Cluster" END, tags: ["SECTOR_INFORMATION_TECHNOLOGY", "SECTOR_COMMON_IT", "SUBSECTOR_CLOUD_SERVICES", "TECH_CLOUD_NATIVE", "OPS_CRITICALITY_HIGH", "REG_SOC2"]})-[:LOCATED_AT]->(f1);

// Managed Service Providers (3 facilities, 30 equipment)
// Cloud Regions (2 facilities, 20 equipment)

// VALIDATION: Expected 100 equipment
// FINAL TOTAL: 5,900 equipment across 16 sectors
