// GAP-004 FIXED: RevenueModel and CustomerImpact deployment
// File: gap004_revenuemodel_customerimpact_fixed.cypher
// Created: 2025-11-13
// Purpose: Deploy RevenueModel (with fixed seasonalFactors) and CustomerImpact nodes

// ==============================================================================
// CG-9 Node Type 3: RevenueModel (10 samples) - FIXED seasonalFactors
// ==============================================================================

// Sample 1: High-Speed Rail Revenue
CREATE (revenue1:RevenueModel {
  modelId: "revenue-high-speed-rail",
  modelName: "High-Speed Rail Revenue",
  revenuePerHour: 125000.0,
  revenuePerPassenger: 45.0,
  revenuePerTrip: 27000.0,
  currency: "EUR",
  seasonalFactors: '{"january":0.7,"february":0.75,"march":0.85,"april":0.9,"may":1.0,"june":1.1,"july":1.3,"august":1.25,"september":1.0,"october":0.95,"november":0.8,"december":1.5}',
  peakHourMultiplier: 1.4,
  assetType: "TRAIN",
  annualRevenue: 1095000000.0,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Freight Transport Revenue
CREATE (revenue2:RevenueModel {
  modelId: "revenue-freight-transport",
  modelName: "Freight Transport Revenue",
  revenuePerHour: 75000.0,
  revenuePerTrip: 180000.0,
  currency: "EUR",
  seasonalFactors: '{"january":1.1,"february":1.0,"march":1.0,"april":0.95,"may":0.9,"june":0.9,"july":0.85,"august":0.8,"september":0.95,"october":1.05,"november":1.15,"december":1.2}',
  peakHourMultiplier: 1.0,
  assetType: "TRAIN",
  annualRevenue: 657000000.0,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 3: Water Utility Revenue
CREATE (revenue3:RevenueModel {
  modelId: "revenue-water-utility",
  modelName: "Water Supply Revenue",
  revenuePerHour: 7500.0,
  currency: "EUR",
  seasonalFactors: '{"january":0.9,"february":0.9,"march":0.95,"april":1.0,"may":1.1,"june":1.2,"july":1.3,"august":1.25,"september":1.1,"october":1.0,"november":0.95,"december":0.9}',
  peakHourMultiplier: 1.5,
  assetType: "TRACK",
  annualRevenue: 65700000.0,
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 4: Power Grid Revenue
CREATE (revenue4:RevenueModel {
  modelId: "revenue-power-grid",
  modelName: "Electrical Power Sales",
  revenuePerHour: 416667.0,
  currency: "EUR",
  seasonalFactors: '{"january":1.2,"february":1.15,"march":1.0,"april":0.95,"may":0.9,"june":0.95,"july":1.1,"august":1.15,"september":0.95,"october":0.9,"november":1.05,"december":1.3}',
  peakHourMultiplier: 1.8,
  assetType: "STATION",
  annualRevenue: 3650004000.0,
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// Sample 5: Manufacturing Production Revenue
CREATE (revenue5:RevenueModel {
  modelId: "revenue-manufacturing",
  modelName: "Manufacturing Production",
  revenuePerHour: 50000.0,
  currency: "USD",
  seasonalFactors: '{"january":0.95,"february":1.0,"march":1.05,"april":1.1,"may":1.1,"june":1.05,"july":0.9,"august":0.85,"september":1.05,"october":1.1,"november":1.15,"december":0.95}',
  peakHourMultiplier: 1.0,
  assetType: "STATION",
  annualRevenue: 438000000.0,
  customer_namespace: "customer:Manufacturing-Lambda",
  is_shared: false
});

// Sample 6: Building Rental Revenue
CREATE (revenue6:RevenueModel {
  modelId: "revenue-building-rental",
  modelName: "Commercial Building Rental",
  revenuePerHour: 4167.0,
  currency: "USD",
  seasonalFactors: '{"january":1.0,"february":1.0,"march":1.0,"april":1.0,"may":1.0,"june":1.0,"july":1.0,"august":1.0,"september":1.0,"october":1.0,"november":1.0,"december":1.0}',
  peakHourMultiplier: 1.0,
  assetType: "STATION",
  annualRevenue: 36500000.0,
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 7: Gas Pipeline Revenue
CREATE (revenue7:RevenueModel {
  modelId: "revenue-gas-pipeline",
  modelName: "Natural Gas Transport",
  revenuePerHour: 177083.0,
  currency: "EUR",
  seasonalFactors: '{"january":1.4,"february":1.35,"march":1.2,"april":1.0,"may":0.85,"june":0.75,"july":0.7,"august":0.7,"september":0.85,"october":1.0,"november":1.2,"december":1.45}',
  peakHourMultiplier: 1.3,
  assetType: "TRACK",
  annualRevenue: 1551247000.0,
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// Sample 8: Data Center Hosting Revenue
CREATE (revenue8:RevenueModel {
  modelId: "revenue-datacenter-hosting",
  modelName: "Data Center Hosting",
  revenuePerHour: 41667.0,
  currency: "USD",
  seasonalFactors: '{"january":1.0,"february":1.0,"march":1.0,"april":1.0,"may":1.0,"june":1.0,"july":1.0,"august":1.0,"september":1.0,"october":1.0,"november":1.0,"december":1.0}',
  peakHourMultiplier: 1.0,
  assetType: "STATION",
  annualRevenue: 365004000.0,
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// Sample 9: Telecom Services Revenue
CREATE (revenue9:RevenueModel {
  modelId: "revenue-telecom-services",
  modelName: "Telecommunications Services",
  revenuePerHour: 208333.0,
  currency: "USD",
  seasonalFactors: '{"january":1.0,"february":1.0,"march":1.0,"april":1.0,"may":1.0,"june":1.0,"july":1.05,"august":1.05,"september":1.0,"october":1.0,"november":1.05,"december":1.1}',
  peakHourMultiplier: 1.2,
  assetType: "STATION",
  annualRevenue: 1825002000.0,
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// Sample 10: Station Operations Revenue
CREATE (revenue10:RevenueModel {
  modelId: "revenue-station-ops",
  modelName: "Railway Station Operations",
  revenuePerHour: 12500.0,
  currency: "EUR",
  seasonalFactors: '{"january":0.8,"february":0.85,"march":0.9,"april":1.0,"may":1.1,"june":1.2,"july":1.4,"august":1.35,"september":1.1,"october":1.0,"november":0.9,"december":1.3}',
  peakHourMultiplier: 1.6,
  assetType: "STATION",
  annualRevenue: 109500000.0,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// ==============================================================================
// CG-9 Node Type 4: CustomerImpact (10 samples) - ALREADY CLEAN
// ==============================================================================

// Sample 1: Railway Signal System Customer Impact
CREATE (impact1:CustomerImpact {
  impactId: "impact-customers-signal-20251113",
  disruptionEventId: "disruption-signal-system-20251113",
  affectedCustomers: ["passenger-group-morning-commuters"],
  customerCount: 82800,
  affectedDuration: duration('PT3H'),
  impactType: "SERVICE_CANCELLATION",
  impactSeverity: "CRITICAL",
  compensationDue: 2070000.0,
  compensationCurrency: "EUR",
  compensationBasis: "EU Passenger Rights Regulation 261/2004 - Article 7",
  compensationPerCustomer: 25.0,
  compensationPaid: false,
  reputationImpact: "HIGH",
  customerComplaintCount: 1247,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Water Supply Customer Impact
CREATE (impact2:CustomerImpact {
  impactId: "impact-customers-water-20251113",
  disruptionEventId: "disruption-water-supply-20251113",
  affectedCustomers: ["residential-district-north"],
  customerCount: 82000,
  affectedDuration: duration('PT6H'),
  impactType: "COMPLETE_OUTAGE",
  impactSeverity: "CRITICAL",
  compensationDue: 82000.0,
  compensationCurrency: "EUR",
  compensationBasis: "Municipal Water Service Agreement - Section 5.2",
  compensationPerCustomer: 1.0,
  compensationPaid: false,
  reputationImpact: "HIGH",
  customerComplaintCount: 3450,
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 3: Power Outage Customer Impact
CREATE (impact3:CustomerImpact {
  impactId: "impact-customers-power-20251113",
  disruptionEventId: "disruption-power-outage-20251113",
  affectedCustomers: ["commercial-zone-central", "residential-district-south"],
  customerCount: 250000,
  affectedDuration: duration('PT12H'),
  impactType: "COMPLETE_OUTAGE",
  impactSeverity: "CRITICAL",
  compensationDue: 1250000.0,
  compensationCurrency: "EUR",
  compensationBasis: "Power Supply Regulations - Outage Compensation",
  compensationPerCustomer: 5.0,
  compensationPaid: false,
  reputationImpact: "CRITICAL",
  customerComplaintCount: 12350,
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// Sample 4: Building Climate Control Impact
CREATE (impact4:CustomerImpact {
  impactId: "impact-customers-hvac-20251113",
  disruptionEventId: "disruption-hvac-failure-20251113",
  affectedCustomers: ["building-tenants"],
  customerCount: 2500,
  affectedDuration: duration('PT24H'),
  impactType: "DEGRADED_SERVICE",
  impactSeverity: "HIGH",
  compensationDue: 125000.0,
  compensationCurrency: "USD",
  compensationBasis: "Building Lease Agreement - Service Level Clause",
  compensationPerCustomer: 50.0,
  compensationPaid: false,
  reputationImpact: "HIGH",
  customerComplaintCount: 456,
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 5: Gas Pipeline Customer Impact
CREATE (impact5:CustomerImpact {
  impactId: "impact-customers-gas-20251113",
  disruptionEventId: "disruption-gas-pipeline-20251113",
  affectedCustomers: ["industrial-customers", "residential-gas-users"],
  customerCount: 15000,
  affectedDuration: duration('PT48H'),
  impactType: "DELAY",
  impactSeverity: "HIGH",
  compensationDue: 75000.0,
  compensationCurrency: "EUR",
  compensationBasis: "Gas Supply Contract - Compensation Terms",
  compensationPerCustomer: 5.0,
  compensationPaid: false,
  reputationImpact: "MEDIUM",
  customerComplaintCount: 890,
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// Sample 6: Manufacturing Delay Impact
CREATE (impact6:CustomerImpact {
  impactId: "impact-customers-mfg-20251113",
  disruptionEventId: "disruption-manufacturing-20251113",
  affectedCustomers: ["automotive-oem-customer"],
  customerCount: 1,
  affectedDuration: duration('PT24H'),
  impactType: "DELAY",
  impactSeverity: "CRITICAL",
  compensationDue: 500000.0,
  compensationCurrency: "USD",
  compensationBasis: "Supply Contract - Late Delivery Penalty",
  compensationPerCustomer: 500000.0,
  compensationPaid: false,
  reputationImpact: "CRITICAL",
  customerComplaintCount: 1,
  customer_namespace: "customer:Manufacturing-Lambda",
  is_shared: false
});

// Sample 7: Rail Freight Delay Impact
CREATE (impact7:CustomerImpact {
  impactId: "impact-customers-freight-20251113",
  disruptionEventId: "disruption-freight-delay-20251113",
  affectedCustomers: ["logistics-company-a", "logistics-company-b", "logistics-company-c"],
  customerCount: 3,
  affectedDuration: duration('PT8H'),
  impactType: "DELAY",
  impactSeverity: "HIGH",
  compensationDue: 150000.0,
  compensationCurrency: "EUR",
  compensationBasis: "Freight Transport Agreement - Delay Compensation",
  compensationPerCustomer: 50000.0,
  compensationPaid: false,
  reputationImpact: "MEDIUM",
  customerComplaintCount: 3,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 8: Data Center Outage Impact
CREATE (impact8:CustomerImpact {
  impactId: "impact-customers-datacenter-20251113",
  disruptionEventId: "disruption-datacenter-20251113",
  affectedCustomers: ["enterprise-customers"],
  customerCount: 150,
  affectedDuration: duration('PT2H'),
  impactType: "DEGRADED_SERVICE",
  impactSeverity: "MEDIUM",
  compensationDue: 300000.0,
  compensationCurrency: "USD",
  compensationBasis: "Hosting SLA - Availability Credits",
  compensationPerCustomer: 2000.0,
  compensationPaid: false,
  reputationImpact: "MEDIUM",
  customerComplaintCount: 45,
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// Sample 9: Telecom Service Impact
CREATE (impact9:CustomerImpact {
  impactId: "impact-customers-telecom-20251113",
  disruptionEventId: "disruption-telecom-20251113",
  affectedCustomers: ["residential-subscribers", "business-subscribers"],
  customerCount: 500000,
  affectedDuration: duration('PT4H'),
  impactType: "DEGRADED_SERVICE",
  impactSeverity: "HIGH",
  compensationDue: 2000000.0,
  compensationCurrency: "USD",
  compensationBasis: "Service Level Agreement - Downtime Credits",
  compensationPerCustomer: 4.0,
  compensationPaid: false,
  reputationImpact: "HIGH",
  customerComplaintCount: 25600,
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// Sample 10: Station Services Impact
CREATE (impact10:CustomerImpact {
  impactId: "impact-customers-station-20251113",
  disruptionEventId: "disruption-station-services-20251113",
  affectedCustomers: ["station-visitors"],
  customerCount: 15000,
  affectedDuration: duration('PT3H'),
  impactType: "DEGRADED_SERVICE",
  impactSeverity: "MEDIUM",
  compensationDue: 75000.0,
  compensationCurrency: "EUR",
  compensationBasis: "Station Services Agreement - Convenience Compensation",
  compensationPerCustomer: 5.0,
  compensationPaid: false,
  reputationImpact: "LOW",
  customerComplaintCount: 234,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// ==============================================================================
// END OF FIXED DEPLOYMENT
// ==============================================================================
// Expected: 20 nodes created (10 RevenueModel + 10 CustomerImpact)
// ==============================================================================
