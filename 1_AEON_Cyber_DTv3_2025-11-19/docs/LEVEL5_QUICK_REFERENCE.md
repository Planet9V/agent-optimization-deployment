# LEVEL 5: INFORMATION STREAMS - QUICK REFERENCE

One-page reference for accessing and querying Level 5 data.

---

## 🚀 DATABASE ACCESS

```bash
# Connect to Neo4j
docker exec -it openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg'

# Run query from command line
docker exec openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg' "YOUR_QUERY_HERE"

# Execute deployment script
cat /path/to/level5_deployment.cypher | docker exec -i openspg-neo4j cypher-shell -u neo4j -p 'neo4j@openspg'
```

---

## 📊 QUICK STATS

```cypher
// Total Level 5 nodes
MATCH (n) WHERE any(label IN labels(n) WHERE label IN [
  'InformationStream', 'DataSource', 'DataConsumer', 'DataProcessor',
  'QualityMetric', 'PerformanceMetric', 'SLA', 'Alert'
])
RETURN count(n);
// Result: 9,905 nodes

// Total Level 5 relationships
MATCH ()-[r]->() WHERE type(r) IN [
  'CONSUMES_FROM', 'PROCESSES_THROUGH', 'DELIVERS_TO', 'CHAINS_TO',
  'MONITORS', 'MEASURES', 'GOVERNS', 'MONITORS_EQUIPMENT',
  'TRACKS_PROCESS', 'DETECTS_VULNERABILITY', 'IDENTIFIES_THREAT',
  'INSTALLED_ON', 'USES_SOFTWARE'
]
RETURN count(r);
// Result: 3,179,673 relationships
```

---

## 🎯 TOP 10 MOST USEFUL QUERIES

### 1. List All Stream Types
```cypher
MATCH (s:InformationStream)
RETURN s.streamType, count(*) as Count
ORDER BY Count DESC;
```

### 2. Find Critical Real-Time Streams
```cypher
MATCH (s:RealTimeStream)
WHERE s.priority = 'critical'
RETURN s.name, s.protocol, s.dataRate, s.latency
LIMIT 10;
```

### 3. Equipment Monitoring Overview
```cypher
MATCH (s:InformationStream)-[:MONITORS_EQUIPMENT]->(e:Equipment)
RETURN s.name, s.streamType, count(e) as EquipmentCount
ORDER BY EquipmentCount DESC
LIMIT 10;
```

### 4. Security Threat Detection
```cypher
MATCH (s:SecurityStream)-[:IDENTIFIES_THREAT]->(t:Threat)
RETURN s.name, s.monitoringType, count(t) as Threats
ORDER BY Threats DESC
LIMIT 10;
```

### 5. Active Alerts by Severity
```cypher
MATCH (a:Alert)
WHERE a.status = 'active'
RETURN a.severity, count(*) as Count
ORDER BY CASE a.severity
  WHEN 'critical' THEN 1
  WHEN 'high' THEN 2
  WHEN 'medium' THEN 3
  ELSE 4 END;
```

### 6. Processing Pipeline Visualization
```cypher
MATCH path = (s:InformationStream)-[:PROCESSES_THROUGH]->(p1:DataProcessor)-[:CHAINS_TO]->(p2:DataProcessor)
RETURN s.name, p1.name, p1.processorType, p2.name, p2.processorType
LIMIT 10;
```

### 7. Data Quality Status
```cypher
MATCH (qm:QualityMetric)
RETURN qm.metricType, qm.status, count(*) as Count
ORDER BY Count DESC;
```

### 8. Performance Metrics Summary
```cypher
MATCH (pm:PerformanceMetric)-[:MEASURES]->(s:InformationStream)
RETURN pm.metricType, avg(toFloat(pm.currentValue)) as AvgValue, pm.unit
ORDER BY AvgValue DESC;
```

### 9. SLA Compliance
```cypher
MATCH (sla:SLA)
WHERE toFloat(sla.current) < toFloat(sla.target)
RETURN sla.name, sla.slaType, sla.target, sla.current
ORDER BY toFloat(sla.target) - toFloat(sla.current) DESC;
```

### 10. End-to-End Data Flow
```cypher
MATCH (src:DataSource)<-[:CONSUMES_FROM]-(s:InformationStream)-[:PROCESSES_THROUGH]->(p:DataProcessor),
      (s)-[:DELIVERS_TO]->(c:DataConsumer)
RETURN src.name, s.name, p.name, c.name
LIMIT 10;
```

---

## 📋 NODE TYPES & COUNTS

| Node Type | Count | Description |
|-----------|-------|-------------|
| Alert | 4,100 | System alerts and notifications |
| DataProcessor | 1,500 | Data transformation nodes |
| DataSource | 1,205 | Data origin points |
| DataConsumer | 1,200 | Data destination points |
| InformationStream | 600 | Stream definitions |
| QualityMetric | 500 | Data quality measures |
| PerformanceMetric | 500 | Performance measures |
| SLA | 300 | Service level agreements |

---

## 🔗 RELATIONSHIP TYPES

### Internal Relationships
- `CONSUMES_FROM` (289,050): Stream → DataSource
- `PROCESSES_THROUGH` (270,203): Stream → DataProcessor
- `CHAINS_TO` (225,358): Processor → Processor
- `DELIVERS_TO` (216,126): Stream → DataConsumer
- `MONITORS` (195,265): QualityMetric → Stream
- `MEASURES` (165,400): PerformanceMetric → Stream
- `GOVERNS` (53,862): SLA → Stream

### Integration Relationships
- `INSTALLED_ON` (968,125): SensorSource → Device
- `TRACKS_PROCESS` (344,256): Stream → Process
- `MONITORS_EQUIPMENT` (289,233): Stream → Equipment
- `USES_SOFTWARE` (149,949): Consumer → SoftwareComponent
- `IDENTIFIES_THREAT` (9,762): SecurityStream → Threat
- `DETECTS_VULNERABILITY` (3,084): SecurityStream → CVE

---

## 🔍 COMMON FILTERS

### By Stream Type
```cypher
WHERE s.streamType IN ['real-time', 'batch', 'event-driven', 'analytics', 'integration', 'security']
```

### By Priority
```cypher
WHERE s.priority IN ['critical', 'high', 'medium', 'low']
```

### By Protocol
```cypher
WHERE s.protocol IN ['Modbus TCP', 'OPC UA', 'MQTT', 'DNP3']
```

### By Alert Severity
```cypher
WHERE a.severity IN ['critical', 'high', 'medium', 'low']
```

### By Alert Status
```cypher
WHERE a.status IN ['active', 'acknowledged', 'resolved']
```

---

## 📁 DOCUMENTATION FILES

1. **LEVEL5_DEPLOYMENT_COMPLETE.md** - Executive summary and overview
2. **LEVEL5_DEPLOYMENT_VALIDATION.md** - Detailed validation results
3. **LEVEL5_QUERY_GUIDE.md** - 50+ query examples by category
4. **LEVEL5_QUICK_REFERENCE.md** - This file (quick reference)

**Location**: `/home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/docs/`

---

## 🛠️ DEPLOYMENT FILES

1. **level5_deployment.cypher** - Complete deployment script
   - Location: `/home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/scripts/`
   - Use: Redeployment, testing, or reference

---

## 💡 TROUBLESHOOTING

### Query Running Slow?
```cypher
// Check if indexes exist
SHOW INDEXES;

// Create missing index
CREATE INDEX stream_id IF NOT EXISTS FOR (s:InformationStream) ON (s.id);
```

### Find Disconnected Nodes
```cypher
// Sources not connected to streams
MATCH (ds:DataSource)
WHERE NOT (ds)<-[:CONSUMES_FROM]-()
RETURN ds.name LIMIT 10;

// Consumers not receiving data
MATCH (dc:DataConsumer)
WHERE NOT (dc)<-[:DELIVERS_TO]-()
RETURN dc.name LIMIT 10;
```

### Verify Integration
```cypher
// Check equipment connections
MATCH (s:InformationStream)-[:MONITORS_EQUIPMENT]->(e:Equipment)
RETURN count(*) as ConnectionCount;

// Check CVE connections
MATCH (s:SecurityStream)-[:DETECTS_VULNERABILITY]->(cve:CVE)
RETURN count(*) as CVEConnections;
```

---

## 🎯 COMMON USE CASES

### Real-Time Dashboard Query
```cypher
MATCH (s:RealTimeStream)-[:DELIVERS_TO]->(d:Dashboard)
WHERE s.priority = 'critical'
RETURN s.name, s.dataRate, s.latency, d.name
ORDER BY s.latency ASC;
```

### Security Monitoring
```cypher
MATCH (s:SecurityStream)-[:IDENTIFIES_THREAT]->(t:Threat)
WHERE s.monitoringType = 'intrusion-detection'
RETURN s.name, count(t) as ThreatCount
ORDER BY ThreatCount DESC;
```

### Process Analytics
```cypher
MATCH (s:AnalyticsStream)-[:TRACKS_PROCESS]->(p:Process)
RETURN s.name, s.analyticsType, p.name
LIMIT 20;
```

### Quality Assurance
```cypher
MATCH (qm:QualityMetric)-[:MONITORS]->(s:InformationStream)
WHERE qm.status = 'failed'
RETURN qm.name, qm.metricType, s.name
ORDER BY qm.name;
```

---

## 📊 EXPORT EXAMPLES

### Export to CSV (conceptual)
```cypher
// Export stream configuration
MATCH (s:InformationStream)
RETURN s.id, s.name, s.streamType, s.protocol, s.priority
ORDER BY s.name;

// Export integration mapping
MATCH (s:InformationStream)-[r]->(target)
WHERE type(r) IN ['MONITORS_EQUIPMENT', 'TRACKS_PROCESS']
RETURN s.name, type(r), target.name;
```

---

## 🔐 INDEX REFERENCE

All Level 5 indexes for optimal performance:

```cypher
CREATE INDEX stream_id IF NOT EXISTS FOR (s:InformationStream) ON (s.id);
CREATE INDEX stream_type IF NOT EXISTS FOR (s:InformationStream) ON (s.streamType);
CREATE INDEX source_id IF NOT EXISTS FOR (ds:DataSource) ON (ds.id);
CREATE INDEX consumer_id IF NOT EXISTS FOR (dc:DataConsumer) ON (dc.id);
CREATE INDEX processor_id IF NOT EXISTS FOR (dp:DataProcessor) ON (dp.id);
CREATE INDEX quality_id IF NOT EXISTS FOR (qm:QualityMetric) ON (qm.id);
CREATE INDEX perf_id IF NOT EXISTS FOR (pm:PerformanceMetric) ON (pm.id);
CREATE INDEX sla_id IF NOT EXISTS FOR (sla:SLA) ON (sla.id);
CREATE INDEX alert_id IF NOT EXISTS FOR (a:Alert) ON (a.id);
```

---

**Version**: 1.0
**Last Updated**: 2025-11-23
**Status**: ✅ Production Ready
