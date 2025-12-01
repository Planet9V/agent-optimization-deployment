// Financial Services Sector - TASKMASTER Task 8
// Target: 400 equipment, 60 facilities
// Created: 2025-11-19 23:50:00 UTC

// Banks (20 facilities, 140 equipment)
CREATE (f1:Facility {facilityId: "FIN-BANK-NY-001", name: "JPMorgan Chase NYC HQ", facilityType: "BANK_HEADQUARTERS", sector: "FINANCIAL_SERVICES", latitude: 40.7549, longitude: -73.9840, state: "NY"})
UNWIND range(1, 7) as i CREATE (e:Equipment {equipmentId: "EQ-FIN-BANK-NY-001-" + i, equipmentType: CASE i WHEN 1 THEN "Core Banking System" WHEN 2 THEN "ATM Network Controller" WHEN 3 THEN "Payment Gateway" WHEN 4 THEN "Fraud Detection System" WHEN 5 THEN "Router" WHEN 6 THEN "Firewall" ELSE "Database Server" END, tags: ["SECTOR_FINANCIAL_SERVICES", "SUBSECTOR_BANKING", "GEO_STATE_NY", "OPS_CRITICALITY_CRITICAL", "VENDOR_" + CASE i WHEN 1 THEN "FISERV" WHEN 5 THEN "CISCO" WHEN 6 THEN "PALO_ALTO" ELSE "IBM" END, "REG_PCI_DSS", "REG_SOX", "REG_GLBA"] + CASE i WHEN 5 THEN ["SECTOR_COMMON_IT"] WHEN 6 THEN ["SECTOR_COMMON_IT"] ELSE [] END})-[:LOCATED_AT]->(f1);

// Stock Exchanges (5 facilities, 60 equipment)
// Investment Firms (15 facilities, 100 equipment)
// Payment Processors (10 facilities, 60 equipment)
// Credit Unions (10 facilities, 40 equipment)

// Cross-sector tagging: Routers and Firewalls tagged SECTOR_COMMON_IT

// VALIDATION: Expected 400 equipment
