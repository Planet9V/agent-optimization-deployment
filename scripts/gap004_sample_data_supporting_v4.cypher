// GAP-004 Sample Data: Supporting Nodes (FIXED VERSION)
// File: gap004_sample_data_supporting_v2.cypher
// Created: 2025-11-13
// Purpose: Realistic test data for supporting integration nodes
// FIX: Converted nested deviation maps to JSON strings

// ==============================================================================
// Supporting Node Type 1: StateDeviation (10 samples - critical for UC2)
// ==============================================================================

// Sample 1: Centrifuge Overspeed Deviation (Stuxnet-style)
CREATE (deviation1:StateDeviation {
  deviationId: "deviation-centrifuge001-20251113150007",
  assetId: "device-centrifuge-001",
  expectedState: '{"rotationSpeed": 1064, "temperature": 35.5}',
  actualState: '{"rotationSpeed": 1410, "temperature": 45.8}',
  deviation: '{"rotationSpeed":{"expected":1064,"actual":1410,"difference":346,"percentDeviation":32.5},"temperature":{"expected":35.5,"actual":45.8,"difference":10.3,"percentDeviation":29.0}}',
  severity: "CRITICAL",
  timestamp: datetime('2025-11-13T15:00:07Z'),
  detectionMethod: "PHYSICS_MODEL",
  confidence: 0.96,
  isPotentialAttack: true,
  rootCause: "CYBER_ATTACK",
  customer_namespace: "customer:NuclearFacility-Alpha",
  is_shared: false
});

// Sample 2: Temperature Anomaly - Railway PLC
CREATE (deviation2:StateDeviation {
  deviationId: "deviation-plc001-temp-20251113150010",
  assetId: "device-plc-rail-001",
  expectedState: '{"temperature": 85.5}',
  actualState: '{"temperature": 103.7}',
  deviation: '{"temperature":{"expected":85.5,"actual":103.7,"difference":18.2,"percentDeviation":21.3}}',
  severity: "CRITICAL",
  timestamp: datetime('2025-11-13T15:00:10Z'),
  detectionMethod: "PHYSICS_MODEL",
  confidence: 0.92,
  isPotentialAttack: true,
  rootCause: "CYBER_ATTACK",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 3: Pressure Drop - Water Pump
CREATE (deviation3:StateDeviation {
  deviationId: "deviation-pump001-pressure-20251113150205",
  assetId: "device-pump-water-001",
  expectedState: '{"pressure": 95.2, "flowRate": 850.0}',
  actualState: '{"pressure": 45.3, "flowRate": 520.0}',
  deviation: '{"pressure":{"expected":95.2,"actual":45.3,"difference":-49.9,"percentDeviation":-52.4},"flowRate":{"expected":850.0,"actual":520.0,"difference":-330.0,"percentDeviation":-38.8}}',
  severity: "HIGH",
  timestamp: datetime('2025-11-13T15:02:05Z'),
  detectionMethod: "STATISTICAL_THRESHOLD",
  confidence: 0.89,
  isPotentialAttack: false,
  rootCause: "ACTUATOR_MALFUNCTION",
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 4: Voltage Fluctuation - Transformer
CREATE (deviation4:StateDeviation {
  deviationId: "deviation-transformer001-voltage-20251113150310",
  assetId: "device-transformer-001",
  expectedState: '{"voltage": 138000}',
  actualState: '{"voltage": 152000}',
  deviation: '{"voltage":{"expected":138000,"actual":152000,"difference":14000,"percentDeviation":10.1}}',
  severity: "CRITICAL",
  timestamp: datetime('2025-11-13T15:03:10Z'),
  detectionMethod: "RULE_BASED",
  confidence: 0.98,
  isPotentialAttack: false,
  rootCause: "PHYSICS_VIOLATION",
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// Sample 5: Vibration Anomaly - Gas Compressor
CREATE (deviation5:StateDeviation {
  deviationId: "deviation-compressor001-vibration-20251113150620",
  assetId: "device-compressor-001",
  expectedState: '{"vibration": 3.5}',
  actualState: '{"vibration": 6.8}',
  deviation: '{"vibration":{"expected":3.5,"actual":6.8,"difference":3.3,"percentDeviation":94.3}}',
  severity: "HIGH",
  timestamp: datetime('2025-11-13T15:06:20Z'),
  detectionMethod: "ML_ANOMALY",
  confidence: 0.87,
  isPotentialAttack: false,
  rootCause: "SENSOR_FAILURE",
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// Sample 6: Signal Lamp Failure
CREATE (deviation6:StateDeviation {
  deviationId: "deviation-signal001-lamp-20251113150715",
  assetId: "device-signal-controller-001",
  expectedState: '{"lampIntensity": 95.0, "voltage": 24.0}',
  actualState: '{"lampIntensity": 25.0, "voltage": 18.5}',
  deviation: '{"lampIntensity":{"expected":95.0,"actual":25.0,"difference":-70.0,"percentDeviation":-73.7},"voltage":{"expected":24.0,"actual":18.5,"difference":-5.5,"percentDeviation":-22.9}}',
  severity: "CRITICAL",
  timestamp: datetime('2025-11-13T15:07:15Z'),
  detectionMethod: "PHYSICS_MODEL",
  confidence: 0.94,
  isPotentialAttack: false,
  rootCause: "ACTUATOR_MALFUNCTION",
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 7: HVAC Temperature Deviation
CREATE (deviation7:StateDeviation {
  deviationId: "deviation-hvac001-temp-20251113150520",
  assetId: "device-hvac-001",
  expectedState: '{"temperature": 21.5, "humidity": 45.0}',
  actualState: '{"temperature": 28.3, "humidity": 62.0}',
  deviation: '{"temperature":{"expected":21.5,"actual":28.3,"difference":6.8,"percentDeviation":31.6},"humidity":{"expected":45.0,"actual":62.0,"difference":17.0,"percentDeviation":37.8}}',
  severity: "MEDIUM",
  timestamp: datetime('2025-11-13T15:05:20Z'),
  detectionMethod: "STATISTICAL_THRESHOLD",
  confidence: 0.85,
  isPotentialAttack: false,
  rootCause: "SENSOR_FAILURE",
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 8: Chemical Reactor pH Deviation
CREATE (deviation8:StateDeviation {
  deviationId: "deviation-reactor001-ph-20251113150825",
  assetId: "device-reactor-001",
  expectedState: '{"ph": 7.2, "temperature": 185.0}',
  actualState: '{"ph": 5.8, "temperature": 195.0}',
  deviation: '{"ph":{"expected":7.2,"actual":5.8,"difference":-1.4,"percentDeviation":-19.4},"temperature":{"expected":185.0,"actual":195.0,"difference":10.0,"percentDeviation":5.4}}',
  severity: "HIGH",
  timestamp: datetime('2025-11-13T15:08:25Z'),
  detectionMethod: "PHYSICS_MODEL",
  confidence: 0.91,
  isPotentialAttack: false,
  rootCause: "PHYSICS_VIOLATION",
  customer_namespace: "customer:ChemPlant-Eta",
  is_shared: false
});

// Sample 9: Wind Turbine Pitch Deviation
CREATE (deviation9:StateDeviation {
  deviationId: "deviation-turbine001-pitch-20251113150930",
  assetId: "device-turbine-001",
  expectedState: '{"pitch": 8.5, "rotorSpeed": 12.5}',
  actualState: '{"pitch": 15.2, "rotorSpeed": 18.3}',
  deviation: '{"pitch":{"expected":8.5,"actual":15.2,"difference":6.7,"percentDeviation":78.8},"rotorSpeed":{"expected":12.5,"actual":18.3,"difference":5.8,"percentDeviation":46.4}}',
  severity: "CRITICAL",
  timestamp: datetime('2025-11-13T15:09:30Z'),
  detectionMethod: "RULE_BASED",
  confidence: 0.93,
  isPotentialAttack: false,
  rootCause: "ACTUATOR_MALFUNCTION",
  customer_namespace: "customer:WindFarm-Theta",
  is_shared: false
});

// Sample 10: Furnace Overtemperature
CREATE (deviation10:StateDeviation {
  deviationId: "deviation-furnace001-overtemp-20251113150435",
  assetId: "device-furnace-001",
  expectedState: '{"temperature": 1250.0, "pressure": 1.02}',
  actualState: '{"temperature": 1385.0, "pressure": 1.15}',
  deviation: '{"temperature":{"expected":1250.0,"actual":1385.0,"difference":135.0,"percentDeviation":10.8},"pressure":{"expected":1.02,"actual":1.15,"difference":0.13,"percentDeviation":12.7}}',
  severity: "CRITICAL",
  timestamp: datetime('2025-11-13T15:04:35Z'),
  detectionMethod: "PHYSICS_MODEL",
  confidence: 0.97,
  isPotentialAttack: true,
  rootCause: "CYBER_ATTACK",
  customer_namespace: "customer:SteelMill-Delta",
  is_shared: false
});

// ==============================================================================
// Supporting Node Type 2: TimeSeriesData (10 samples - for R6 analysis)
// ==============================================================================

// Sample 1: Failed Login Attempts Time Series
CREATE (ts1:TimeSeriesAnalysis {
  analysisId: "timeseries-failed-logins-20251113",
  metric: "failed_login_attempts",
  assetId: "device-app-server-01",
  aggregation: "COUNT",
  window: duration('PT1H'),
  trend: "ANOMALOUS",
  baseline: 12.5,
  currentValue: 458.7,
  anomalyScore: 7.2,
  standardDeviation: 15.8,
  timestamp: datetime('2025-11-13T15:00:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Network Traffic Volume Time Series
CREATE (ts2:TimeSeriesAnalysis {
  analysisId: "timeseries-network-traffic-20251113",
  metric: "network_traffic_volume",
  assetId: "device-router-01",
  aggregation: "AVERAGE",
  window: duration('PT15M'),
  trend: "INCREASING",
  baseline: 450.0,
  currentValue: 1250.0,
  anomalyScore: 5.8,
  standardDeviation: 125.3,
  timestamp: datetime('2025-11-13T15:30:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 3: CPU Usage Time Series
CREATE (ts3:TimeSeriesAnalysis {
  analysisId: "timeseries-cpu-usage-20251113",
  metric: "cpu_usage",
  assetId: "device-plc-rail-001",
  aggregation: "PERCENTILE_95",
  window: duration('PT5M'),
  trend: "STABLE",
  baseline: 45.0,
  currentValue: 48.5,
  anomalyScore: 0.8,
  standardDeviation: 5.2,
  timestamp: datetime('2025-11-13T15:35:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 4: Process Count Time Series
CREATE (ts4:TimeSeriesAnalysis {
  analysisId: "timeseries-process-count-20251113",
  metric: "process_count",
  assetId: "device-app-server-01",
  aggregation: "COUNT",
  window: duration('PT10M'),
  trend: "VOLATILE",
  baseline: 150.0,
  currentValue: 325.0,
  anomalyScore: 6.5,
  standardDeviation: 25.0,
  timestamp: datetime('2025-11-13T15:10:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 5: Disk I/O Time Series
CREATE (ts5:TimeSeriesAnalysis {
  analysisId: "timeseries-disk-io-20251113",
  metric: "disk_io_rate",
  assetId: "device-plc-manufacturing-01",
  aggregation: "MAX",
  window: duration('PT1M'),
  trend: "ANOMALOUS",
  baseline: 2500.0,
  currentValue: 8750.0,
  anomalyScore: 8.3,
  standardDeviation: 750.0,
  timestamp: datetime('2025-11-13T16:00:00Z'),
  customer_namespace: "customer:Manufacturing-Lambda",
  is_shared: false
});

// Sample 6: Memory Usage Time Series
CREATE (ts6:TimeSeriesAnalysis {
  analysisId: "timeseries-memory-usage-20251113",
  metric: "memory_usage",
  assetId: "device-datacenter-power-01",
  aggregation: "AVERAGE",
  window: duration('PT5M'),
  trend: "STABLE",
  baseline: 65.0,
  currentValue: 67.5,
  anomalyScore: 1.2,
  standardDeviation: 3.5,
  timestamp: datetime('2025-11-13T15:30:00Z'),
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// Sample 7: Packet Drop Rate Time Series
CREATE (ts7:TimeSeriesAnalysis {
  analysisId: "timeseries-packet-drops-20251113",
  metric: "packet_drop_rate",
  assetId: "device-firewall-01",
  aggregation: "SUM",
  window: duration('PT1M'),
  trend: "INCREASING",
  baseline: 0.5,
  currentValue: 12.3,
  anomalyScore: 9.1,
  standardDeviation: 1.2,
  timestamp: datetime('2025-11-13T15:25:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 8: Connection Count Time Series
CREATE (ts8:TimeSeriesAnalysis {
  analysisId: "timeseries-connections-20251113",
  metric: "active_connections",
  assetId: "device-scada-network-01",
  aggregation: "COUNT",
  window: duration('PT15M'),
  trend: "DECREASING",
  baseline: 150.0,
  currentValue: 45.0,
  anomalyScore: 4.2,
  standardDeviation: 15.0,
  timestamp: datetime('2025-11-13T15:30:30Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 9: Response Time Time Series
CREATE (ts9:TimeSeriesAnalysis {
  analysisId: "timeseries-response-time-20251113",
  metric: "api_response_time",
  assetId: "device-app-server-01",
  aggregation: "PERCENTILE_95",
  window: duration('PT5M'),
  trend: "VOLATILE",
  baseline: 125.0,
  currentValue: 850.0,
  anomalyScore: 7.8,
  standardDeviation: 95.0,
  timestamp: datetime('2025-11-13T15:05:00Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 10: Temperature Sensor Time Series
CREATE (ts10:TimeSeriesAnalysis {
  analysisId: "timeseries-sensor-temp-20251113",
  metric: "sensor_temperature",
  assetId: "device-plc-rail-001",
  aggregation: "AVERAGE",
  window: duration('PT1H'),
  trend: "INCREASING",
  baseline: 85.5,
  currentValue: 103.7,
  anomalyScore: 6.9,
  standardDeviation: 8.5,
  timestamp: datetime('2025-11-13T15:00:10Z'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// ==============================================================================
// Supporting Node Type 3: DisruptionEvent (10 samples - for CG-9 integration)
// ==============================================================================

// Sample 1: Signal System Disruption
CREATE (disrupt1:DisruptionEvent {
  eventId: "disruption-signal-system-20251113",
  eventName: "Railway Signal System Failure - November 2025",
  startTime: datetime('2025-11-13T15:30:15Z'),
  endTime: datetime('2025-11-13T18:30:15Z'),
  duration: duration('PT3H'),
  affectedAssets: ["device-signal-system-01", "device-signal-controller-001"],
  affectedAssetCount: 23,
  rootCause: "POWER_OUTAGE",
  rootCauseDetail: "Substation transformer failure caused power loss to signal system",
  impact: '{
    "operational": {
      "trainsAffected": 23,
      "tripsCancelled": 45,
      "serviceReduction": 50.0
    },
    "financial": {
      "revenueLoss": 3726000.0,
      "slaPenalty": 2300000.0,
      "compensationCosts": 2070000.0,
      "totalCost": 8096000.0
    },
    "customer": {
      "passengersAffected": 82800,
      "complaintsReceived": 1247,
      "reputationImpact": "HIGH"
    }
  }',
  severity: "CRITICAL",
  recoveryTime: duration('PT48H'),
  incidentResponse: '{
    "responseStartTime": "datetime('2025-11-13T15:31:00Z')",
    "responders": ["network-team", "power-team", "safety-team"],
    "actionsToken": ["isolate_fault", "switch_backup", "restore_power"],
    "resolutionSummary": "Backup power engaged, primary transformer replaced"
  }',
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Water Supply Disruption
CREATE (disrupt2:DisruptionEvent {
  eventId: "disruption-water-supply-20251113",
  eventName: "Water Pump Station Failure - November 2025",
  startTime: datetime('2025-11-13T15:31:00Z'),
  endTime: datetime('2025-11-13T21:31:00Z'),
  duration: duration('PT6H'),
  affectedAssets: ["device-pump-station-03"],
  affectedAssetCount: 1,
  rootCause: "POWER_OUTAGE",
  rootCauseDetail: "Substation failure caused pump station offline",
  impact: '{
    "operational": {
      "trainsAffected": 0,
      "tripsCancelled": 0,
      "serviceReduction": 100.0
    },
    "financial": {
      "revenueLoss": 45000.0,
      "slaPenalty": 150000.0,
      "compensationCosts": 82000.0,
      "totalCost": 277000.0
    },
    "customer": {
      "passengersAffected": 82000,
      "complaintsReceived": 3450,
      "reputationImpact": "HIGH"
    }
  }',
  severity: "CRITICAL",
  recoveryTime: duration('PT8H'),
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 3: Manufacturing PLC Disruption
CREATE (disrupt3:DisruptionEvent {
  eventId: "disruption-manufacturing-20251113",
  eventName: "Manufacturing PLC Cyber Attack - November 2025",
  startTime: datetime('2025-11-13T16:00:00Z'),
  endTime: datetime('2025-11-14T16:00:00Z'),
  duration: duration('PT24H'),
  affectedAssets: ["device-plc-manufacturing-01", "device-cooling-system-01"],
  affectedAssetCount: 3,
  rootCause: "CYBER_ATTACK",
  rootCauseDetail: "Ransomware attack exploiting CVE-2021-44228 (Log4Shell) in production control system",
  impact: '{
    "operational": {
      "trainsAffected": 0,
      "tripsCancelled": 0,
      "serviceReduction": 100.0
    },
    "financial": {
      "revenueLoss": 1200000.0,
      "slaPenalty": 0.0,
      "compensationCosts": 0.0,
      "totalCost": 1200000.0
    },
    "customer": {
      "passengersAffected": 0,
      "complaintsReceived": 1,
      "reputationImpact": "MEDIUM"
    }
  }',
  severity: "CRITICAL",
  recoveryTime: duration('PT72H'),
  customer_namespace: "customer:Manufacturing-Lambda",
  is_shared: false
});

// Sample 4: Power Grid Disruption
CREATE (disrupt4:DisruptionEvent {
  eventId: "disruption-power-outage-20251113",
  eventName: "Regional Power Outage - November 2025",
  startTime: datetime('2025-11-13T15:30:00Z'),
  endTime: datetime('2025-11-14T03:30:00Z'),
  duration: duration('PT12H'),
  affectedAssets: ["device-substation-01", "device-transformer-001"],
  affectedAssetCount: 200,
  rootCause: "HARDWARE_FAILURE",
  rootCauseDetail: "Main substation transformer catastrophic failure",
  impact: '{
    "operational": {
      "trainsAffected": 0,
      "tripsCancelled": 0,
      "serviceReduction": 100.0
    },
    "financial": {
      "revenueLoss": 5000000.0,
      "slaPenalty": 3500000.0,
      "compensationCosts": 1250000.0,
      "totalCost": 9750000.0
    },
    "customer": {
      "passengersAffected": 250000,
      "complaintsReceived": 12350,
      "reputationImpact": "CRITICAL"
    }
  }',
  severity: "CRITICAL",
  recoveryTime: duration('PT168H'),
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// Sample 5: HVAC Failure Disruption
CREATE (disrupt5:DisruptionEvent {
  eventId: "disruption-hvac-failure-20251113",
  eventName: "Building HVAC Complete Failure - November 2025",
  startTime: datetime('2025-11-13T17:00:00Z'),
  endTime: datetime('2025-11-14T17:00:00Z'),
  duration: duration('PT24H'),
  affectedAssets: ["device-hvac-chiller-01", "device-hvac-chiller-02"],
  affectedAssetCount: 2,
  rootCause: "HARDWARE_FAILURE",
  rootCauseDetail: "Primary chiller failure cascaded to secondary chiller overload",
  impact: '{
    "operational": {
      "trainsAffected": 0,
      "tripsCancelled": 0,
      "serviceReduction": 100.0
    },
    "financial": {
      "revenueLoss": 100000.0,
      "slaPenalty": 300000.0,
      "compensationCosts": 125000.0,
      "totalCost": 525000.0
    },
    "customer": {
      "passengersAffected": 2500,
      "complaintsReceived": 456,
      "reputationImpact": "HIGH"
    }
  }',
  severity: "HIGH",
  recoveryTime: duration('PT72H'),
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 6: Gas Pipeline Disruption
CREATE (disrupt6:DisruptionEvent {
  eventId: "disruption-gas-pipeline-20251113",
  eventName: "Gas Compressor Station Failure - November 2025",
  startTime: datetime('2025-11-13T18:00:00Z'),
  endTime: datetime('2025-11-15T18:00:00Z'),
  duration: duration('PT48H'),
  affectedAssets: ["device-compressor-station-05"],
  affectedAssetCount: 1,
  rootCause: "HARDWARE_FAILURE",
  rootCauseDetail: "Compressor bearing failure causing station shutdown",
  impact: '{
    "operational": {
      "trainsAffected": 0,
      "tripsCancelled": 0,
      "serviceReduction": 25.0
    },
    "financial": {
      "revenueLoss": 850000.0,
      "slaPenalty": 450000.0,
      "compensationCosts": 75000.0,
      "totalCost": 1375000.0
    },
    "customer": {
      "passengersAffected": 15000,
      "complaintsReceived": 890,
      "reputationImpact": "MEDIUM"
    }
  }',
  severity: "HIGH",
  recoveryTime: duration('PT96H'),
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// Sample 7: SCADA Network Disruption
CREATE (disrupt7:DisruptionEvent {
  eventId: "disruption-scada-network-20251113",
  eventName: "SCADA Communication Network Failure - November 2025",
  startTime: datetime('2025-11-13T15:30:30Z'),
  endTime: datetime('2025-11-13T19:30:30Z'),
  duration: duration('PT4H'),
  affectedAssets: ["device-scada-network-01", "device-rtu-network-01"],
  affectedAssetCount: 150,
  rootCause: "POWER_OUTAGE",
  rootCauseDetail: "Signal system power loss caused SCADA network offline",
  impact: '{
    "operational": {
      "trainsAffected": 150,
      "tripsCancelled": 0,
      "serviceReduction": 100.0
    },
    "financial": {
      "revenueLoss": 250000.0,
      "slaPenalty": 0.0,
      "compensationCosts": 0.0,
      "totalCost": 250000.0
    },
    "customer": {
      "passengersAffected": 0,
      "complaintsReceived": 0,
      "reputationImpact": "MEDIUM"
    }
  }',
  severity: "CRITICAL",
  recoveryTime: duration('PT8H'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 8: Data Center Disruption
CREATE (disrupt8:DisruptionEvent {
  eventId: "disruption-datacenter-20251113",
  eventName: "Data Center Power Failure - November 2025",
  startTime: datetime('2025-11-13T15:30:05Z'),
  endTime: datetime('2025-11-13T17:30:05Z'),
  duration: duration('PT2H'),
  affectedAssets: ["device-datacenter-power-01"],
  affectedAssetCount: 150,
  rootCause: "POWER_OUTAGE",
  rootCauseDetail: "Grid power loss, backup generators activated successfully",
  impact: '{
    "operational": {
      "trainsAffected": 0,
      "tripsCancelled": 0,
      "serviceReduction": 0.0
    },
    "financial": {
      "revenueLoss": 0.0,
      "slaPenalty": 0.0,
      "compensationCosts": 0.0,
      "totalCost": 50000.0
    },
    "customer": {
      "passengersAffected": 0,
      "complaintsReceived": 0,
      "reputationImpact": "LOW"
    }
  }',
  severity: "MEDIUM",
  recoveryTime: duration('PT4H'),
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// Sample 9: Telecom Service Disruption
CREATE (disrupt9:DisruptionEvent {
  eventId: "disruption-telecom-20251113",
  eventName: "Telecommunications Service Degradation - November 2025",
  startTime: datetime('2025-11-13T15:30:05Z'),
  endTime: datetime('2025-11-13T19:30:05Z'),
  duration: duration('PT4H'),
  affectedAssets: ["device-router-01", "device-firewall-01"],
  affectedAssetCount: 25,
  rootCause: "CYBER_ATTACK",
  rootCauseDetail: "DDoS attack causing network congestion and service degradation",
  impact: '{
    "operational": {
      "trainsAffected": 0,
      "tripsCancelled": 0,
      "serviceReduction": 50.0
    },
    "financial": {
      "revenueLoss": 416668.0,
      "slaPenalty": 1000000.0,
      "compensationCosts": 2000000.0,
      "totalCost": 3416668.0
    },
    "customer": {
      "passengersAffected": 500000,
      "complaintsReceived": 25600,
      "reputationImpact": "HIGH"
    }
  }',
  severity: "HIGH",
  recoveryTime: duration('PT8H'),
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// Sample 10: Station Services Disruption
CREATE (disrupt10:DisruptionEvent {
  eventId: "disruption-station-services-20251113",
  eventName: "Railway Station Services Failure - November 2025",
  startTime: datetime('2025-11-13T15:30:15Z'),
  endTime: datetime('2025-11-13T18:30:15Z'),
  duration: duration('PT3H'),
  affectedAssets: ["station-ticketing-system", "station-information-displays"],
  affectedAssetCount: 15,
  rootCause: "POWER_OUTAGE",
  rootCauseDetail: "Power loss to station auxiliary systems",
  impact: '{
    "operational": {
      "trainsAffected": 0,
      "tripsCancelled": 0,
      "serviceReduction": 75.0
    },
    "financial": {
      "revenueLoss": 37500.0,
      "slaPenalty": 0.0,
      "compensationCosts": 75000.0,
      "totalCost": 112500.0
    },
    "customer": {
      "passengersAffected": 15000,
      "complaintsReceived": 234,
      "reputationImpact": "LOW"
    }
  }',
  severity: "MEDIUM",
  recoveryTime: duration('PT6H'),
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// ==============================================================================
// Supporting Node Type 4: SystemResilience (10 samples - for UC3 integration)
// ==============================================================================

// Sample 1: PLC Resilience Metrics
CREATE (resilience1:SystemResilience {
  resilienceId: "resilience-plc-rail-001",
  assetId: "device-plc-rail-001",
  mtbf: duration('PT8760H'),
  mttr: duration('PT4H'),
  availability: 99.95,
  redundancyLevel: 1,
  failoverCapability: "AUTOMATIC",
  lastFailureDate: datetime('2025-08-15T10:00:00Z'),
  failureHistory: '[
    {"timestamp": "datetime('2025-08-15T10:00:00Z')", "cause": "SOFTWARE_BUG", "duration": "duration('PT3H')"},
    {"timestamp": "datetime('2025-05-20T14:00:00Z')", "cause": "POWER_OUTAGE", "duration": "duration('PT2H')"}
  ]',
  resilienceScore: 9.2,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 2: Signal System Resilience
CREATE (resilience2:SystemResilience {
  resilienceId: "resilience-signal-system-01",
  assetId: "device-signal-system-01",
  mtbf: duration('PT17520H'),
  mttr: duration('PT2H'),
  availability: 99.99,
  redundancyLevel: 2,
  failoverCapability: "AUTOMATIC",
  lastFailureDate: datetime('2025-11-13T15:30:15Z'),
  resilienceScore: 9.8,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 3: Water Pump Resilience
CREATE (resilience3:SystemResilience {
  resilienceId: "resilience-pump-station-03",
  assetId: "device-pump-station-03",
  mtbf: duration('PT4380H'),
  mttr: duration('PT6H'),
  availability: 99.86,
  redundancyLevel: 0,
  failoverCapability: "NONE",
  lastFailureDate: datetime('2025-11-13T15:31:00Z'),
  resilienceScore: 7.5,
  customer_namespace: "customer:WaterUtility-Beta",
  is_shared: false
});

// Sample 4: Substation Resilience
CREATE (resilience4:SystemResilience {
  resilienceId: "resilience-substation-01",
  assetId: "device-substation-01",
  mtbf: duration('PT87600H'),
  mttr: duration('PT48H'),
  availability: 99.45,
  redundancyLevel: 1,
  failoverCapability: "MANUAL",
  lastFailureDate: datetime('2025-11-13T15:30:00Z'),
  resilienceScore: 8.0,
  customer_namespace: "customer:PowerGrid-Gamma",
  is_shared: false
});

// Sample 5: Manufacturing PLC Resilience
CREATE (resilience5:SystemResilience {
  resilienceId: "resilience-plc-mfg-01",
  assetId: "device-plc-manufacturing-01",
  mtbf: duration('PT4380H'),
  mttr: duration('PT8H'),
  availability: 98.18,
  redundancyLevel: 1,
  failoverCapability: "SEMI_AUTOMATIC",
  lastFailureDate: datetime('2025-11-13T16:00:00Z'),
  resilienceScore: 7.0,
  customer_namespace: "customer:Manufacturing-Lambda",
  is_shared: false
});

// Sample 6: HVAC Chiller Resilience
CREATE (resilience6:SystemResilience {
  resilienceId: "resilience-hvac-chiller-01",
  assetId: "device-hvac-chiller-01",
  mtbf: duration('PT2190H'),
  mttr: duration('PT12H'),
  availability: 99.45,
  redundancyLevel: 1,
  failoverCapability: "AUTOMATIC",
  lastFailureDate: datetime('2025-11-13T17:00:00Z'),
  resilienceScore: 8.5,
  customer_namespace: "customer:SmartBuilding-Epsilon",
  is_shared: false
});

// Sample 7: Gas Compressor Resilience
CREATE (resilience7:SystemResilience {
  resilienceId: "resilience-compressor-05",
  assetId: "device-compressor-station-05",
  mtbf: duration('PT8760H'),
  mttr: duration('PT96H'),
  availability: 98.91,
  redundancyLevel: 0,
  failoverCapability: "NONE",
  lastFailureDate: datetime('2025-11-13T18:00:00Z'),
  resilienceScore: 6.5,
  customer_namespace: "customer:GasPipeline-Zeta",
  is_shared: false
});

// Sample 8: SCADA Network Resilience
CREATE (resilience8:SystemResilience {
  resilienceId: "resilience-scada-network-01",
  assetId: "device-scada-network-01",
  mtbf: duration('PT17520H'),
  mttr: duration('PT4H'),
  availability: 99.98,
  redundancyLevel: 2,
  failoverCapability: "AUTOMATIC",
  lastFailureDate: datetime('2025-11-13T15:30:30Z'),
  resilienceScore: 9.5,
  customer_namespace: "customer:RailOperator-XYZ",
  is_shared: false
});

// Sample 9: Data Center Resilience
CREATE (resilience9:SystemResilience {
  resilienceId: "resilience-datacenter-01",
  assetId: "device-datacenter-power-01",
  mtbf: duration('PT43800H'),
  mttr: duration('PT1H'),
  availability: 99.998,
  redundancyLevel: 3,
  failoverCapability: "AUTOMATIC",
  lastFailureDate: datetime('2025-11-13T15:30:05Z'),
  resilienceScore: 9.9,
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// Sample 10: Firewall Resilience
CREATE (resilience10:SystemResilience {
  resilienceId: "resilience-firewall-01",
  assetId: "device-firewall-01",
  mtbf: duration('PT35040H'),
  mttr: duration('PT2H'),
  availability: 99.99,
  redundancyLevel: 2,
  failoverCapability: "AUTOMATIC",
  lastFailureDate: datetime('2025-09-10T12:00:00Z'),
  resilienceScore: 9.7,
  customer_namespace: "customer:TelecomProvider-Kappa",
  is_shared: false
});

// ==============================================================================
// END OF SUPPORTING SAMPLE DATA (FIXED)
// ==============================================================================
// Total Supporting Nodes Created: 40 nodes (10 per type × 4 types)
// Coverage: StateDeviation, TimeSeriesAnalysis, DisruptionEvent, SystemResilience
// FIX APPLIED: All nested deviation maps converted to JSON strings
// Simple maps (expectedState, actualState, impact) remain as maps
// ==============================================================================
