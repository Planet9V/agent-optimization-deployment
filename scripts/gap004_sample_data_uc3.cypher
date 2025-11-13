// GAP-004 Sample Data: UC3 Cascading Failure Simulation
// File: gap004_sample_data_uc3.cypher
// Created: 2025-11-13
// Purpose: Realistic test data for UC3 nodes (4 types, 10+ samples each)

// ==============================================================================
// UC3 Node Type 1: CascadeEvent (10 samples)
// ==============================================================================

// Sample 1: Primary Power Failure - Substation
CREATE (cascade1:CascadeEvent {
  eventId: "cascade-sim001-001",
  simulationId: "sim001-power-failure",
  sequenceNumber: 1,
  timestamp: datetime('2025-11-13T15:30:00Z'),
  failedAssetId: "device-substation-01",
  causeAssetId: "external-grid",
  causeType: "PRIMARY_FAILURE",
  propagationProbability: 1.0,
  propagationDelay: duration('PT0S'),
  impactSummary: "Main substation transformer failure - 50MW capacity offline",
  consequences: ["POWER_LOSS", "SAFETY_IMPACT"],
  severity: "CRITICAL",
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// Sample 2: Railway Signal System Offline
CREATE (cascade2:CascadeEvent {
  eventId: "cascade-sim001-002",
  simulationId: "sim001-power-failure",
  sequenceNumber: 2,
  timestamp: datetime('2025-11-13T15:30:15Z'),
  failedAssetId: "device-signal-system-01",
  causeAssetId: "device-substation-01",
  causeType: "POWER_LOSS",
  propagationProbability: 0.95,
  propagationDelay: duration('PT15S'),
  impactSummary: "Railway signal system offline, 23 trains affected",
  consequences: ["SERVICE_DISRUPTION", "SAFETY_IMPACT", "REVENUE_LOSS"],
  severity: "CRITICAL",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 3: SCADA Communication Loss
CREATE (cascade3:CascadeEvent {
  eventId: "cascade-sim001-003",
  simulationId: "sim001-power-failure",
  sequenceNumber: 3,
  timestamp: datetime('2025-11-13T15:30:30Z'),
  failedAssetId: "device-scada-network-01",
  causeAssetId: "device-signal-system-01",
  causeType: "COMM_LOSS",
  propagationProbability: 0.85,
  propagationDelay: duration('PT15S'),
  impactSummary: "SCADA network offline, 150 RTUs disconnected",
  consequences: ["CONTROL_LOSS", "SERVICE_DISRUPTION"],
  severity: "HIGH",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 4: Water Pump Station Failure
CREATE (cascade4:CascadeEvent {
  eventId: "cascade-sim001-004",
  simulationId: "sim001-power-failure",
  sequenceNumber: 4,
  timestamp: datetime('2025-11-13T15:31:00Z'),
  failedAssetId: "device-pump-station-03",
  causeAssetId: "device-substation-01",
  causeType: "POWER_LOSS",
  propagationProbability: 0.90,
  propagationDelay: duration('PT60S'),
  impactSummary: "Water distribution pump failure, 82,000 customers affected",
  consequences: ["SERVICE_DISRUPTION", "SAFETY_IMPACT"],
  severity: "CRITICAL",
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 5: Data Center Backup Power Activation
CREATE (cascade5:CascadeEvent {
  eventId: "cascade-sim001-005",
  simulationId: "sim001-power-failure",
  sequenceNumber: 5,
  timestamp: datetime('2025-11-13T15:30:05Z'),
  failedAssetId: "device-datacenter-power-01",
  causeAssetId: "device-substation-01",
  causeType: "POWER_LOSS",
  propagationProbability: 1.0,
  propagationDelay: duration('PT5S'),
  impactSummary: "Data center switched to backup generators - 2 hour fuel supply",
  consequences: ["SERVICE_DEGRADATION"],
  severity: "MEDIUM",
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// Sample 6: Manufacturing Plant Shutdown
CREATE (cascade6:CascadeEvent {
  eventId: "cascade-sim002-001",
  simulationId: "sim002-cyber-attack",
  sequenceNumber: 1,
  timestamp: datetime('2025-11-13T16:00:00Z'),
  failedAssetId: "device-plc-manufacturing-01",
  causeAssetId: "attacker-workstation",
  causeType: "CYBER_ATTACK",
  propagationProbability: 0.75,
  propagationDelay: duration('PT0S'),
  impactSummary: "PLC compromised via Log4Shell - production line halted",
  consequences: ["SERVICE_DISRUPTION", "REVENUE_LOSS"],
  severity: "HIGH",
  customer_namespace: "customer:Manufacturing-Lambda",
  is_shared: false
});

// Sample 7: Cooling System Failure
CREATE (cascade7:CascadeEvent {
  eventId: "cascade-sim002-002",
  simulationId: "sim002-cyber-attack",
  sequenceNumber: 2,
  timestamp: datetime('2025-11-13T16:02:30Z'),
  failedAssetId: "device-cooling-system-01",
  causeAssetId: "device-plc-manufacturing-01",
  causeType: "CONTROL_LOSS",
  propagationProbability: 0.80,
  propagationDelay: duration('PT150S'),
  impactSummary: "Cooling system offline - temperature rising in production area",
  consequences: ["SAFETY_IMPACT", "EQUIPMENT_DAMAGE"],
  severity: "HIGH",
  customer_namespace: "customer:Manufacturing-Lambda",
  is_shared: false
});

// Sample 8: Building HVAC Failure
CREATE (cascade8:CascadeEvent {
  eventId: "cascade-sim003-001",
  simulationId: "sim003-hvac-cascade",
  sequenceNumber: 1,
  timestamp: datetime('2025-11-13T17:00:00Z'),
  failedAssetId: "device-hvac-chiller-01",
  causeAssetId: "device-hvac-chiller-01",
  causeType: "PRIMARY_FAILURE",
  propagationProbability: 1.0,
  propagationDelay: duration('PT0S'),
  impactSummary: "Primary chiller failure - 25-story building affected",
  consequences: ["COMFORT_IMPACT", "SAFETY_IMPACT"],
  severity: "MEDIUM",
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 9: Secondary Chiller Overload
CREATE (cascade9:CascadeEvent {
  eventId: "cascade-sim003-002",
  simulationId: "sim003-hvac-cascade",
  sequenceNumber: 2,
  timestamp: datetime('2025-11-13T17:10:00Z'),
  failedAssetId: "device-hvac-chiller-02",
  causeAssetId: "device-hvac-chiller-01",
  causeType: "CONTROL_LOSS",
  propagationProbability: 0.70,
  propagationDelay: duration('PT600S'),
  impactSummary: "Secondary chiller overloaded and failed - complete HVAC offline",
  consequences: ["SERVICE_DISRUPTION", "EVACUATION_REQUIRED"],
  severity: "HIGH",
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 10: Gas Pipeline Compressor Cascade
CREATE (cascade10:CascadeEvent {
  eventId: "cascade-sim004-001",
  simulationId: "sim004-gas-pipeline",
  sequenceNumber: 1,
  timestamp: datetime('2025-11-13T18:00:00Z'),
  failedAssetId: "device-compressor-station-05",
  causeAssetId: "device-compressor-station-05",
  causeType: "PRIMARY_FAILURE",
  propagationProbability: 1.0,
  propagationDelay: duration('PT0S'),
  impactSummary: "Compressor station 5 offline - pressure drop in pipeline",
  consequences: ["SERVICE_DEGRADATION", "PRESSURE_LOSS"],
  severity: "HIGH",
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// ==============================================================================
// UC3 Node Type 2: DependencyLink (10 samples)
// ==============================================================================

// Sample 1: Power Dependency - Substation → Signal System
CREATE (dep1:DependencyLink {
  linkId: "dep-substation01-signal01-power",
  sourceAssetId: "device-substation-01",
  targetAssetId: "device-signal-system-01",
  dependencyType: "POWER",
  strength: 0.95,
  criticality: "CRITICAL",
  redundancyLevel: 1,
  failoverCapability: true,
  failoverTime: duration('PT30S'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Communication Dependency - Signal System → SCADA
CREATE (dep2:DependencyLink {
  linkId: "dep-signal01-scada01-comm",
  sourceAssetId: "device-signal-system-01",
  targetAssetId: "device-scada-network-01",
  dependencyType: "COMMUNICATION",
  strength: 0.90,
  criticality: "HIGH",
  redundancyLevel: 2,
  failoverCapability: true,
  failoverTime: duration('PT10S'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 3: Power Dependency - Substation → Water Pump
CREATE (dep3:DependencyLink {
  linkId: "dep-substation01-pump03-power",
  sourceAssetId: "device-substation-01",
  targetAssetId: "device-pump-station-03",
  dependencyType: "POWER",
  strength: 0.98,
  criticality: "CRITICAL",
  redundancyLevel: 0,
  failoverCapability: false,
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 4: Power Dependency - Substation → Data Center
CREATE (dep4:DependencyLink {
  linkId: "dep-substation01-datacenter01-power",
  sourceAssetId: "device-substation-01",
  targetAssetId: "device-datacenter-power-01",
  dependencyType: "POWER",
  strength: 1.0,
  criticality: "CRITICAL",
  redundancyLevel: 2,
  failoverCapability: true,
  failoverTime: duration('PT5S'),
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// Sample 5: Control Dependency - PLC → Cooling System
CREATE (dep5:DependencyLink {
  linkId: "dep-plc01-cooling01-control",
  sourceAssetId: "device-plc-manufacturing-01",
  targetAssetId: "device-cooling-system-01",
  dependencyType: "CONTROL",
  strength: 0.85,
  criticality: "HIGH",
  redundancyLevel: 1,
  failoverCapability: true,
  failoverTime: duration('PT60S'),
  customer_namespace: "customer:Manufacturing-Lambda",
  is_shared: false
});

// Sample 6: Physical Dependency - Chiller 1 → Chiller 2
CREATE (dep6:DependencyLink {
  linkId: "dep-chiller01-chiller02-physical",
  sourceAssetId: "device-hvac-chiller-01",
  targetAssetId: "device-hvac-chiller-02",
  dependencyType: "PHYSICAL",
  strength: 0.70,
  criticality: "MEDIUM",
  redundancyLevel: 0,
  failoverCapability: false,
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 7: Data Dependency - SCADA → Control Center
CREATE (dep7:DependencyLink {
  linkId: "dep-scada01-control01-data",
  sourceAssetId: "device-scada-network-01",
  targetAssetId: "device-control-center-01",
  dependencyType: "DATA",
  strength: 0.92,
  criticality: "HIGH",
  redundancyLevel: 1,
  failoverCapability: true,
  failoverTime: duration('PT15S'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 8: Logical Dependency - Firewall → Application Server
CREATE (dep8:DependencyLink {
  linkId: "dep-firewall01-appserver01-logical",
  sourceAssetId: "device-firewall-01",
  targetAssetId: "device-app-server-01",
  dependencyType: "LOGICAL",
  strength: 1.0,
  criticality: "CRITICAL",
  redundancyLevel: 1,
  failoverCapability: true,
  failoverTime: duration('PT1S'),
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// Sample 9: Communication Dependency - Router → RTU Network
CREATE (dep9:DependencyLink {
  linkId: "dep-router01-rtu-network-comm",
  sourceAssetId: "device-router-01",
  targetAssetId: "device-rtu-network-01",
  dependencyType: "COMMUNICATION",
  strength: 0.88,
  criticality: "HIGH",
  redundancyLevel: 2,
  failoverCapability: true,
  failoverTime: duration('PT20S'),
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 10: Power Dependency - Generator → Critical Load
CREATE (dep10:DependencyLink {
  linkId: "dep-generator01-criticalload01-power",
  sourceAssetId: "device-backup-generator-01",
  targetAssetId: "device-critical-load-01",
  dependencyType: "POWER",
  strength: 1.0,
  criticality: "CRITICAL",
  redundancyLevel: 0,
  failoverCapability: false,
  customer_namespace: "customer:DataCenter-Mu",
  is_shared: false
});

// ==============================================================================
// UC3 Node Type 3: PropagationRule (10 samples)
// ==============================================================================

// Sample 1: Power Loss Propagation
CREATE (rule1:PropagationRule {
  ruleId: "rule-power-loss-propagation",
  ruleName: "Power Loss Propagation",
  triggerCondition: "source_availability < 0.1 AND dependency_strength > 0.8",
  propagationProbability: 0.90,
  probabilityAdjustments: {
    redundancyFactor: 0.5,
    failoverFactor: 0.3,
    criticalityFactor: 1.2
  },
  timeDelay: duration('PT15S'),
  delayVariance: duration('PT5S'),
  impactFactor: 1.8,
  applicableDependencyTypes: ["POWER"],
  customer_namespace: "shared:propagation-rules",
  is_shared: true
});

// Sample 2: Communication Failure Cascade
CREATE (rule2:PropagationRule {
  ruleId: "rule-comm-failure-cascade",
  ruleName: "Communication Failure Cascade",
  triggerCondition: "packet_loss > 0.5 AND dependency_strength > 0.7",
  propagationProbability: 0.75,
  probabilityAdjustments: {
    redundancyFactor: 0.6,
    failoverFactor: 0.4,
    criticalityFactor: 1.1
  },
  timeDelay: duration('PT10S'),
  delayVariance: duration('PT3S'),
  impactFactor: 1.5,
  applicableDependencyTypes: ["COMMUNICATION"],
  customer_namespace: "shared:propagation-rules",
  is_shared: true
});

// Sample 3: Control System Cascade
CREATE (rule3:PropagationRule {
  ruleId: "rule-control-system-cascade",
  ruleName: "Control System Cascade",
  triggerCondition: "control_signal_lost AND dependency_type = 'CONTROL'",
  propagationProbability: 0.85,
  probabilityAdjustments: {
    redundancyFactor: 0.5,
    failoverFactor: 0.35,
    criticalityFactor: 1.3
  },
  timeDelay: duration('PT30S'),
  delayVariance: duration('PT10S'),
  impactFactor: 2.0,
  applicableDependencyTypes: ["CONTROL"],
  customer_namespace: "shared:propagation-rules",
  is_shared: true
});

// Sample 4: Cyber Attack Propagation
CREATE (rule4:PropagationRule {
  ruleId: "rule-cyber-attack-propagation",
  ruleName: "Cyber Attack Lateral Movement",
  triggerCondition: "compromised = true AND network_connected = true",
  propagationProbability: 0.65,
  probabilityAdjustments: {
    redundancyFactor: 0.8,
    failoverFactor: 0.7,
    criticalityFactor: 1.0
  },
  timeDelay: duration('PT120S'),
  delayVariance: duration('PT60S'),
  impactFactor: 1.2,
  applicableDependencyTypes: ["COMMUNICATION", "LOGICAL"],
  customer_namespace: "shared:propagation-rules",
  is_shared: true
});

// Sample 5: Physical Failure Propagation
CREATE (rule5:PropagationRule {
  ruleId: "rule-physical-failure-propagation",
  ruleName: "Physical System Failure Propagation",
  triggerCondition: "physical_damage = true AND proximity < 10m",
  propagationProbability: 0.55,
  probabilityAdjustments: {
    redundancyFactor: 0.4,
    failoverFactor: 0.2,
    criticalityFactor: 1.4
  },
  timeDelay: duration('PT60S'),
  delayVariance: duration('PT20S'),
  impactFactor: 1.9,
  applicableDependencyTypes: ["PHYSICAL"],
  customer_namespace: "shared:propagation-rules",
  is_shared: true
});

// Sample 6: Data Feed Loss
CREATE (rule6:PropagationRule {
  ruleId: "rule-data-feed-loss",
  ruleName: "Data Feed Loss Propagation",
  triggerCondition: "data_staleness > 300 AND dependency_type = 'DATA'",
  propagationProbability: 0.70,
  probabilityAdjustments: {
    redundancyFactor: 0.55,
    failoverFactor: 0.45,
    criticalityFactor: 1.15
  },
  timeDelay: duration('PT45S'),
  delayVariance: duration('PT15S'),
  impactFactor: 1.3,
  applicableDependencyTypes: ["DATA"],
  customer_namespace: "shared:propagation-rules",
  is_shared: true
});

// Sample 7: Thermal Cascade
CREATE (rule7:PropagationRule {
  ruleId: "rule-thermal-cascade",
  ruleName: "Thermal Overload Cascade",
  triggerCondition: "temperature > critical_threshold AND cooling_offline = true",
  propagationProbability: 0.80,
  probabilityAdjustments: {
    redundancyFactor: 0.45,
    failoverFactor: 0.30,
    criticalityFactor: 1.5
  },
  timeDelay: duration('PT600S'),
  delayVariance: duration('PT180S'),
  impactFactor: 2.2,
  applicableDependencyTypes: ["PHYSICAL"],
  customer_namespace: "shared:propagation-rules",
  is_shared: true
});

// Sample 8: Voltage Collapse
CREATE (rule8:PropagationRule {
  ruleId: "rule-voltage-collapse",
  ruleName: "Voltage Collapse Propagation",
  triggerCondition: "voltage < 0.9 * nominal AND load_shedding_failed = true",
  propagationProbability: 0.92,
  probabilityAdjustments: {
    redundancyFactor: 0.6,
    failoverFactor: 0.5,
    criticalityFactor: 1.3
  },
  timeDelay: duration('PT5S'),
  delayVariance: duration('PT2S'),
  impactFactor: 2.5,
  applicableDependencyTypes: ["POWER"],
  customer_namespace: "shared:propagation-rules",
  is_shared: true
});

// Sample 9: Backup System Exhaustion
CREATE (rule9:PropagationRule {
  ruleId: "rule-backup-exhaustion",
  ruleName: "Backup System Exhaustion",
  triggerCondition: "backup_fuel < 0.1 AND primary_power_offline = true",
  propagationProbability: 1.0,
  probabilityAdjustments: {
    redundancyFactor: 0.0,
    failoverFactor: 0.0,
    criticalityFactor: 1.0
  },
  timeDelay: duration('PT7200S'),
  delayVariance: duration('PT600S'),
  impactFactor: 3.0,
  applicableDependencyTypes: ["POWER"],
  customer_namespace: "shared:propagation-rules",
  is_shared: true
});

// Sample 10: Network Congestion Cascade
CREATE (rule10:PropagationRule {
  ruleId: "rule-network-congestion",
  ruleName: "Network Congestion Cascade",
  triggerCondition: "network_utilization > 0.95 AND traffic_shaping_disabled = true",
  propagationProbability: 0.68,
  probabilityAdjustments: {
    redundancyFactor: 0.65,
    failoverFactor: 0.50,
    criticalityFactor: 1.1
  },
  timeDelay: duration('PT20S'),
  delayVariance: duration('PT5S'),
  impactFactor: 1.4,
  applicableDependencyTypes: ["COMMUNICATION", "DATA"],
  customer_namespace: "shared:propagation-rules",
  is_shared: true
});

// ==============================================================================
// UC3 Node Type 4: ImpactAssessment (10 samples)
// ==============================================================================

// Sample 1: Railway Signal System Impact
CREATE (impact1:ImpactAssessment {
  impactId: "impact-signal-system-20251113",
  cascadeEventId: "cascade-sim001-002",
  assessmentTimestamp: datetime('2025-11-13T15:31:00Z'),
  operationalImpact: {
    affectedServices: 23,
    affectedCustomers: 82800,
    serviceReduction: 50.0,
    estimatedDowntime: duration('PT3H')
  },
  economicImpact: {
    revenueLoss: 3726000.0,
    currency: "EUR",
    slaPenalty: 2300000.0,
    compensationCosts: 2070000.0,
    totalCost: 8096000.0
  },
  safetyImpact: {
    riskLevel: "MEDIUM",
    affectedPopulation: 82800,
    injuriesEstimated: 0,
    environmentalRisk: false
  },
  recoveryEstimate: {
    estimatedRecoveryTime: duration('PT48H'),
    resourcesRequired: ["technicians:25", "replacement_parts", "backup_power"],
    estimatedCost: 500000.0
  },
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Water Pump Station Impact
CREATE (impact2:ImpactAssessment {
  impactId: "impact-water-pump-20251113",
  cascadeEventId: "cascade-sim001-004",
  assessmentTimestamp: datetime('2025-11-13T15:32:00Z'),
  operationalImpact: {
    affectedServices: 1,
    affectedCustomers: 82000,
    serviceReduction: 100.0,
    estimatedDowntime: duration('PT6H')
  },
  economicImpact: {
    revenueLoss: 45000.0,
    currency: "EUR",
    slaPenalty: 150000.0,
    compensationCosts: 82000.0,
    totalCost: 277000.0
  },
  safetyImpact: {
    riskLevel: "HIGH",
    affectedPopulation: 82000,
    injuriesEstimated: 0,
    environmentalRisk: false
  },
  recoveryEstimate: {
    estimatedRecoveryTime: duration('PT8H'),
    resourcesRequired: ["technicians:10", "backup_generators", "fuel:5000L"],
    estimatedCost: 75000.0
  },
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 3: Manufacturing PLC Impact
CREATE (impact3:ImpactAssessment {
  impactId: "impact-manufacturing-plc-20251113",
  cascadeEventId: "cascade-sim002-001",
  assessmentTimestamp: datetime('2025-11-13T16:01:00Z'),
  operationalImpact: {
    affectedServices: 3,
    affectedCustomers: 0,
    serviceReduction: 100.0,
    estimatedDowntime: duration('PT24H')
  },
  economicImpact: {
    revenueLoss: 1200000.0,
    currency: "USD",
    slaPenalty: 0.0,
    compensationCosts: 0.0,
    totalCost: 1200000.0
  },
  safetyImpact: {
    riskLevel: "MEDIUM",
    affectedPopulation: 250,
    injuriesEstimated: 0,
    environmentalRisk: false
  },
  recoveryEstimate: {
    estimatedRecoveryTime: duration('PT72H'),
    resourcesRequired: ["cybersecurity_team:5", "forensic_analysis", "plc_reimaging"],
    estimatedCost: 250000.0
  },
  customer_namespace: "customer:Manufacturing-Lambda",
  is_shared: false
});

// Sample 4: Data Center Power Impact
CREATE (impact4:ImpactAssessment {
  impactId: "impact-datacenter-power-20251113",
  cascadeEventId: "cascade-sim001-005",
  assessmentTimestamp: datetime('2025-11-13T15:31:00Z'),
  operationalImpact: {
    affectedServices: 150,
    affectedCustomers: 500000,
    serviceReduction: 0.0,
    estimatedDowntime: duration('PT2H')
  },
  economicImpact: {
    revenueLoss: 0.0,
    currency: "USD",
    slaPenalty: 0.0,
    compensationCosts: 0.0,
    totalCost: 50000.0
  },
  safetyImpact: {
    riskLevel: "LOW",
    affectedPopulation: 0,
    injuriesEstimated: 0,
    environmentalRisk: false
  },
  recoveryEstimate: {
    estimatedRecoveryTime: duration('PT4H'),
    resourcesRequired: ["diesel_fuel:5000L", "technicians:3"],
    estimatedCost: 15000.0
  },
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// Sample 5: Cooling System Impact
CREATE (impact5:ImpactAssessment {
  impactId: "impact-cooling-system-20251113",
  cascadeEventId: "cascade-sim002-002",
  assessmentTimestamp: datetime('2025-11-13T16:03:00Z'),
  operationalImpact: {
    affectedServices: 1,
    affectedCustomers: 0,
    serviceReduction: 100.0,
    estimatedDowntime: duration('PT12H')
  },
  economicImpact: {
    revenueLoss: 600000.0,
    currency: "USD",
    slaPenalty: 0.0,
    compensationCosts: 0.0,
    totalCost: 650000.0
  },
  safetyImpact: {
    riskLevel: "HIGH",
    affectedPopulation: 250,
    injuriesEstimated: 0,
    environmentalRisk: true
  },
  environmentalImpact: {
    emissions: 0.0,
    wasteGenerated: 0.0,
    resourceConsumption: 0.0
  },
  recoveryEstimate: {
    estimatedRecoveryTime: duration('PT24H'),
    resourcesRequired: ["hvac_technicians:8", "replacement_chiller", "coolant:500L"],
    estimatedCost: 150000.0
  },
  customer_namespace: "customer:Manufacturing-Lambda",
  is_shared: false
});

// Sample 6: HVAC Chiller 1 Impact
CREATE (impact6:ImpactAssessment {
  impactId: "impact-hvac-chiller1-20251113",
  cascadeEventId: "cascade-sim003-001",
  assessmentTimestamp: datetime('2025-11-13T17:05:00Z'),
  operationalImpact: {
    affectedServices: 1,
    affectedCustomers: 2500,
    serviceReduction: 50.0,
    estimatedDowntime: duration('PT6H')
  },
  economicImpact: {
    revenueLoss: 25000.0,
    currency: "USD",
    slaPenalty: 75000.0,
    compensationCosts: 15000.0,
    totalCost: 115000.0
  },
  safetyImpact: {
    riskLevel: "MEDIUM",
    affectedPopulation: 2500,
    injuriesEstimated: 0,
    environmentalRisk: false
  },
  recoveryEstimate: {
    estimatedRecoveryTime: duration('PT12H'),
    resourcesRequired: ["hvac_technicians:4", "chiller_parts", "refrigerant"],
    estimatedCost: 35000.0
  },
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 7: HVAC Complete Failure Impact
CREATE (impact7:ImpactAssessment {
  impactId: "impact-hvac-complete-20251113",
  cascadeEventId: "cascade-sim003-002",
  assessmentTimestamp: datetime('2025-11-13T17:15:00Z'),
  operationalImpact: {
    affectedServices: 1,
    affectedCustomers: 2500,
    serviceReduction: 100.0,
    estimatedDowntime: duration('PT24H')
  },
  economicImpact: {
    revenueLoss: 100000.0,
    currency: "USD",
    slaPenalty: 300000.0,
    compensationCosts: 125000.0,
    totalCost: 525000.0
  },
  safetyImpact: {
    riskLevel: "CRITICAL",
    affectedPopulation: 2500,
    injuriesEstimated: 3,
    environmentalRisk: false
  },
  recoveryEstimate: {
    estimatedRecoveryTime: duration('PT72H'),
    resourcesRequired: ["hvac_technicians:12", "replacement_chillers:2", "emergency_cooling"],
    estimatedCost: 250000.0
  },
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 8: Gas Compressor Impact
CREATE (impact8:ImpactAssessment {
  impactId: "impact-gas-compressor-20251113",
  cascadeEventId: "cascade-sim004-001",
  assessmentTimestamp: datetime('2025-11-13T18:05:00Z'),
  operationalImpact: {
    affectedServices: 1,
    affectedCustomers: 15000,
    serviceReduction: 25.0,
    estimatedDowntime: duration('PT48H')
  },
  economicImpact: {
    revenueLoss: 850000.0,
    currency: "EUR",
    slaPenalty: 450000.0,
    compensationCosts: 75000.0,
    totalCost: 1375000.0
  },
  safetyImpact: {
    riskLevel: "HIGH",
    affectedPopulation: 15000,
    injuriesEstimated: 0,
    environmentalRisk: false
  },
  recoveryEstimate: {
    estimatedRecoveryTime: duration('PT96H'),
    resourcesRequired: ["technicians:15", "compressor_overhaul", "pipeline_inspection"],
    estimatedCost: 450000.0
  },
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// Sample 9: SCADA Network Impact
CREATE (impact9:ImpactAssessment {
  impactId: "impact-scada-network-20251113",
  cascadeEventId: "cascade-sim001-003",
  assessmentTimestamp: datetime('2025-11-13T15:31:00Z'),
  operationalImpact: {
    affectedServices: 150,
    affectedCustomers: 0,
    serviceReduction: 100.0,
    estimatedDowntime: duration('PT4H')
  },
  economicImpact: {
    revenueLoss: 250000.0,
    currency: "EUR",
    slaPenalty: 0.0,
    compensationCosts: 0.0,
    totalCost: 250000.0
  },
  safetyImpact: {
    riskLevel: "CRITICAL",
    affectedPopulation: 0,
    injuriesEstimated: 0,
    environmentalRisk: false
  },
  recoveryEstimate: {
    estimatedRecoveryTime: duration('PT8H'),
    resourcesRequired: ["network_engineers:8", "backup_communication_links"],
    estimatedCost: 75000.0
  },
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 10: Substation Primary Failure Impact
CREATE (impact10:ImpactAssessment {
  impactId: "impact-substation-primary-20251113",
  cascadeEventId: "cascade-sim001-001",
  assessmentTimestamp: datetime('2025-11-13T15:30:30Z'),
  operationalImpact: {
    affectedServices: 200,
    affectedCustomers: 250000,
    serviceReduction: 100.0,
    estimatedDowntime: duration('PT12H')
  },
  economicImpact: {
    revenueLoss: 5000000.0,
    currency: "EUR",
    slaPenalty: 3500000.0,
    compensationCosts: 1250000.0,
    totalCost: 9750000.0
  },
  safetyImpact: {
    riskLevel: "CRITICAL",
    affectedPopulation: 250000,
    injuriesEstimated: 5,
    environmentalRisk: false
  },
  recoveryEstimate: {
    estimatedRecoveryTime: duration('PT168H'),
    resourcesRequired: ["technicians:50", "replacement_transformer", "specialized_equipment"],
    estimatedCost: 2500000.0
  },
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// ==============================================================================
// END OF UC3 SAMPLE DATA
// ==============================================================================
// Total UC3 Nodes Created: 40 nodes (10 per type × 4 types)
// Coverage: CascadeEvent, DependencyLink, PropagationRule, ImpactAssessment
// Realistic data includes multi-sector cascades, dependencies, propagation logic,
// and comprehensive impact assessments
// ==============================================================================
