# LEVEL 5: INFORMATION STREAMS - QUERY GUIDE

Quick reference for querying Level 5 Information Streams in Neo4j.

---

## 🚀 QUICK START QUERIES

### Count All Level 5 Nodes
```cypher
MATCH (n)
WHERE any(label IN labels(n) WHERE label IN [
  'InformationStream', 'DataSource', 'DataConsumer',
  'DataProcessor', 'QualityMetric', 'PerformanceMetric',
  'SLA', 'Alert'
])
RETURN labels(n)[0] as NodeType, count(*) as Count
ORDER BY Count DESC;
```

### Count All Level 5 Relationships
```cypher
MATCH ()-[r]->()
WHERE type(r) IN [
  'CONSUMES_FROM', 'PROCESSES_THROUGH', 'DELIVERS_TO',
  'CHAINS_TO', 'MONITORS', 'MEASURES', 'GOVERNS',
  'MONITORS_EQUIPMENT', 'TRACKS_PROCESS', 'DETECTS_VULNERABILITY',
  'IDENTIFIES_THREAT', 'INSTALLED_ON', 'USES_SOFTWARE'
]
RETURN type(r) as RelType, count(r) as Count
ORDER BY Count DESC;
```

---

## 📊 STREAM QUERIES

### Find All Real-Time Streams
```cypher
MATCH (s:RealTimeStream)
RETURN s.name, s.protocol, s.dataRate, s.latency, s.priority
ORDER BY s.priority DESC, s.dataRate DESC
LIMIT 20;
```

### Find Critical Streams
```cypher
MATCH (s:InformationStream)
WHERE s.priority = 'critical'
RETURN s.name, s.streamType, s.dataRate, s.latency
ORDER BY s.name;
```

### Find Streams by Protocol
```cypher
MATCH (s:InformationStream)
WHERE s.protocol = 'Modbus TCP'
RETURN s.name, s.streamType, s.dataRate, s.priority
LIMIT 10;
```

### Find High-Throughput Streams
```cypher
MATCH (s:InformationStream)
WHERE toInteger(split(s.dataRate, ' ')[0]) > 1000
RETURN s.name, s.streamType, s.dataRate, s.latency
ORDER BY toInteger(split(s.dataRate, ' ')[0]) DESC
LIMIT 20;
```

---

## 🔗 INTEGRATION QUERIES

### Equipment Monitoring Streams
```cypher
MATCH (s:InformationStream)-[r:MONITORS_EQUIPMENT]->(e:Equipment)
RETURN s.name, s.streamType, r.frequency, e.name
LIMIT 10;
```

### Process Tracking Streams
```cypher
MATCH (s:InformationStream)-[r:TRACKS_PROCESS]->(p:Process)
RETURN s.name, s.streamType, r.granularity, p.name
LIMIT 10;
```

### Security Streams Detecting CVEs
```cypher
MATCH (s:SecurityStream)-[r:DETECTS_VULNERABILITY]->(cve:CVE)
RETURN s.name, s.monitoringType, r.detectionMethod, cve.id
LIMIT 10;
```

### Threat Detection Overview
```cypher
MATCH (s:SecurityStream)-[r:IDENTIFIES_THREAT]->(t:Threat)
RETURN s.name, s.monitoringType, r.confidenceLevel, t.name
ORDER BY r.confidenceLevel DESC
LIMIT 10;
```

### Sensor-Device Mapping
```cypher
MATCH (src:SensorSource)-[r:INSTALLED_ON]->(d:Device)
RETURN src.name, src.sensorType, r.installationDate, d.name
LIMIT 10;
```

---

## 🔄 PIPELINE QUERIES

### Stream Processing Pipelines
```cypher
MATCH path = (s:InformationStream)-[:PROCESSES_THROUGH]->(p:DataProcessor)
RETURN s.name, s.streamType, p.name, p.processorType
LIMIT 10;
```

### Multi-Stage Processing Chains
```cypher
MATCH path = (s:InformationStream)-[:PROCESSES_THROUGH]->(p1:DataProcessor)-[:CHAINS_TO]->(p2:DataProcessor)
RETURN s.name, p1.name, p1.processorType, p2.name, p2.processorType
LIMIT 10;
```

### Complete Stream Flow (Source → Stream → Processor → Consumer)
```cypher
MATCH path = (src:DataSource)<-[:CONSUMES_FROM]-(s:InformationStream)-[:PROCESSES_THROUGH]->(p:DataProcessor)-[:CHAINS_TO*0..1]->(:DataProcessor)<-[:DELIVERS_TO]-(c:DataConsumer)
RETURN src.name, s.name, p.name, c.name
LIMIT 5;
```

### Data Transformation Chains
```cypher
MATCH (t:Transformer)-[:CHAINS_TO*1..3]->(t2:DataProcessor)
RETURN t.name, t.transformationType, collect(t2.name) as ProcessingChain
LIMIT 10;
```

---

## 📈 QUALITY & MONITORING QUERIES

### Quality Metrics Status
```cypher
MATCH (qm:QualityMetric)
RETURN qm.metricType, qm.status, count(*) as Count
ORDER BY Count DESC;
```

### Failed Quality Checks
```cypher
MATCH (qm:QualityMetric)
WHERE qm.status = 'failed'
RETURN qm.name, qm.metricType, qm.threshold, qm.currentValue
ORDER BY qm.name;
```

### Performance Monitoring
```cypher
MATCH (pm:PerformanceMetric)-[:MEASURES]->(s:InformationStream)
RETURN pm.metricType, pm.currentValue, pm.unit, s.name
LIMIT 20;
```

### SLA Compliance
```cypher
MATCH (sla:SLA)-[:GOVERNS]->(s:InformationStream)
RETURN sla.name, sla.slaType, sla.target, sla.current, s.name
ORDER BY sla.current ASC
LIMIT 20;
```

### Active Alerts
```cypher
MATCH (a:Alert)
WHERE a.status = 'active'
RETURN a.name, a.severity, a.alertType, a.created
ORDER BY a.severity, a.created DESC
LIMIT 20;
```

---

## 🎯 ANALYTICAL QUERIES

### Stream Type Distribution
```cypher
MATCH (s:InformationStream)
RETURN s.streamType, count(*) as Count
ORDER BY Count DESC;
```

### Data Source Type Distribution
```cypher
MATCH (ds:DataSource)
RETURN ds.sourceType, count(*) as Count
ORDER BY Count DESC;
```

### Consumer Type Distribution
```cypher
MATCH (dc:DataConsumer)
RETURN dc.consumerType, count(*) as Count
ORDER BY Count DESC;
```

### Processor Type Distribution
```cypher
MATCH (dp:DataProcessor)
RETURN dp.processorType, count(*) as Count
ORDER BY Count DESC;
```

### Most Connected Streams
```cypher
MATCH (s:InformationStream)-[r]-()
WITH s, count(r) as connections
RETURN s.name, s.streamType, connections
ORDER BY connections DESC
LIMIT 20;
```

### Equipment Coverage Analysis
```cypher
MATCH (e:Equipment)
OPTIONAL MATCH (e)<-[:MONITORS_EQUIPMENT]-(s:InformationStream)
WITH e, count(s) as StreamCount
RETURN
  CASE WHEN StreamCount = 0 THEN 'Unmonitored'
       WHEN StreamCount <= 5 THEN 'Low Coverage'
       WHEN StreamCount <= 15 THEN 'Medium Coverage'
       ELSE 'High Coverage' END as Coverage,
  count(e) as EquipmentCount
ORDER BY Coverage;
```

### Security Stream Effectiveness
```cypher
MATCH (s:SecurityStream)
OPTIONAL MATCH (s)-[:DETECTS_VULNERABILITY]->(cve:CVE)
OPTIONAL MATCH (s)-[:IDENTIFIES_THREAT]->(t:Threat)
RETURN s.name, s.monitoringType,
       count(DISTINCT cve) as CVEs,
       count(DISTINCT t) as Threats
ORDER BY CVEs + Threats DESC
LIMIT 20;
```

---

## 🔍 ADVANCED QUERIES

### Find Bottlenecks (Processors with High Load)
```cypher
MATCH (p:DataProcessor)
OPTIONAL MATCH (p)<-[:PROCESSES_THROUGH]-(s:InformationStream)
WITH p, count(s) as StreamCount
WHERE StreamCount > 10
RETURN p.name, p.processorType, StreamCount
ORDER BY StreamCount DESC;
```

### Identify Unused Resources
```cypher
MATCH (ds:DataSource)
WHERE NOT (ds)<-[:CONSUMES_FROM]-(:InformationStream)
RETURN ds.name, ds.sourceType
LIMIT 20;
```

### Find Redundant Consumers
```cypher
MATCH (c:DataConsumer)
OPTIONAL MATCH (c)<-[:DELIVERS_TO]-(s:InformationStream)
WITH c, count(s) as StreamCount
WHERE StreamCount = 0
RETURN c.name, c.consumerType
LIMIT 20;
```

### Critical Path Analysis
```cypher
MATCH path = (s:InformationStream)-[:PROCESSES_THROUGH*1..5]->(p:DataProcessor)
WHERE s.priority = 'critical'
RETURN s.name, length(path) as ProcessingDepth, extract(n IN nodes(path) | n.name) as Pipeline
ORDER BY ProcessingDepth DESC
LIMIT 10;
```

### Data Quality Impact Analysis
```cypher
MATCH (qm:QualityMetric)-[:MONITORS]->(s:InformationStream)-[:DELIVERS_TO]->(c:DataConsumer)
WHERE qm.status = 'failed'
RETURN qm.name, qm.metricType, s.name, collect(c.name) as AffectedConsumers
LIMIT 10;
```

### Compliance Coverage
```cypher
MATCH (sla:SLA)-[:GOVERNS]->(s:InformationStream)
WITH sla, count(s) as StreamsCovered
RETURN sla.slaType, StreamsCovered
ORDER BY StreamsCovered DESC;
```

---

## 🚨 MONITORING & ALERTING QUERIES

### Critical Performance Issues
```cypher
MATCH (pm:PerformanceMetric)-[:MEASURES]->(s:InformationStream)
WHERE toInteger(pm.currentValue) > toInteger(pm.threshold)
RETURN pm.name, pm.metricType, pm.currentValue, pm.threshold, s.name
ORDER BY toInteger(pm.currentValue) - toInteger(pm.threshold) DESC
LIMIT 20;
```

### Security Threats Summary
```cypher
MATCH (a:Alert)
WHERE a.alertType IN ['security-event', 'anomaly-detected'] AND a.status = 'active'
RETURN a.severity, count(*) as AlertCount
ORDER BY AlertCount DESC;
```

### Stream Health Dashboard
```cypher
MATCH (s:InformationStream)
OPTIONAL MATCH (s)<-[qm:MONITORS]-(q:QualityMetric)
OPTIONAL MATCH (s)<-[pm:MEASURES]-(p:PerformanceMetric)
RETURN s.name, s.streamType, s.priority,
       count(DISTINCT q) as QualityChecks,
       count(DISTINCT p) as PerformanceMetrics
ORDER BY s.priority DESC, s.name
LIMIT 20;
```

---

## 📊 EXPORT QUERIES

### Export Stream Configuration
```cypher
MATCH (s:InformationStream)
RETURN s.id, s.name, s.streamType, s.protocol, s.dataRate, s.latency, s.priority, s.encryption
ORDER BY s.name;
```

### Export Integration Mapping
```cypher
MATCH (s:InformationStream)-[r:MONITORS_EQUIPMENT|TRACKS_PROCESS]->(target)
RETURN s.name, type(r) as RelationType, target.name as TargetName
ORDER BY s.name;
```

### Export Processing Pipeline
```cypher
MATCH (s:InformationStream)-[:PROCESSES_THROUGH]->(p:DataProcessor)
RETURN s.name as Stream, p.name as Processor, p.processorType as Type
ORDER BY s.name, p.name;
```

---

## 💡 OPTIMIZATION QUERIES

### Create Composite Index for Performance
```cypher
CREATE INDEX stream_type_priority IF NOT EXISTS
FOR (s:InformationStream) ON (s.streamType, s.priority);
```

### Analyze Relationship Density
```cypher
MATCH (n)
WHERE any(label IN labels(n) WHERE label IN ['InformationStream', 'DataSource', 'DataConsumer', 'DataProcessor'])
RETURN labels(n)[0] as NodeType,
       count(n) as NodeCount,
       count(*) * 1.0 / 9905 * 100 as PercentOfTotal
ORDER BY NodeCount DESC;
```

### Find Most Active Nodes
```cypher
MATCH (n)
WHERE any(label IN labels(n) WHERE label IN ['InformationStream', 'DataSource', 'DataConsumer', 'DataProcessor'])
OPTIONAL MATCH (n)-[r]-()
WITH n, count(r) as RelationshipCount
RETURN labels(n)[0] as NodeType, n.name, RelationshipCount
ORDER BY RelationshipCount DESC
LIMIT 20;
```

---

## 🎯 BUSINESS INTELLIGENCE QUERIES

### Real-Time Monitoring Coverage
```cypher
MATCH (s:RealTimeStream)-[:MONITORS_EQUIPMENT]->(e:Equipment)
WITH s, count(e) as EquipmentCount
RETURN s.name, s.protocol, EquipmentCount
ORDER BY EquipmentCount DESC
LIMIT 20;
```

### Analytics Platform Overview
```cypher
MATCH (aa:AnalyticsApp)<-[:DELIVERS_TO]-(s:AnalyticsStream)
RETURN aa.name, aa.analysisType, count(s) as StreamCount
ORDER BY StreamCount DESC;
```

### Security Monitoring Coverage
```cypher
MATCH (ss:SecurityStream)
OPTIONAL MATCH (ss)-[:DETECTS_VULNERABILITY]->(cve:CVE)
OPTIONAL MATCH (ss)-[:IDENTIFIES_THREAT]->(t:Threat)
RETURN ss.monitoringType,
       count(DISTINCT ss) as Streams,
       count(DISTINCT cve) as CVEsCovered,
       count(DISTINCT t) as ThreatsCovered
ORDER BY Streams DESC;
```

---

**Query Guide Version**: 1.0
**Last Updated**: 2025-11-23
**Total Queries**: 50+
**Coverage**: Streams, Integration, Pipelines, Quality, Monitoring, Analytics, Optimization
