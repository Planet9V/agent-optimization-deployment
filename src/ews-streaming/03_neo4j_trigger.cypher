// =============================================================================
// GAP-ML-005: Neo4j APOC Trigger for EWS Streaming
// =============================================================================
// File: src/ews-streaming/03_neo4j_trigger.cypher
// Created: 2025-11-30
// Purpose: APOC trigger to publish EWS threshold breaches to message queue
// Database: bolt://aeon-neo4j-dev:7687
// Requirements: APOC plugin with apoc.trigger.* procedures
// =============================================================================

// -----------------------------------------------------------------------------
// STEP 1: Verify APOC trigger procedures are available
// -----------------------------------------------------------------------------
CALL apoc.help('trigger') YIELD name, text
RETURN name, text
ORDER BY name;

// Expected procedures:
// - apoc.trigger.add
// - apoc.trigger.list
// - apoc.trigger.remove
// - apoc.trigger.pause
// - apoc.trigger.resume

// -----------------------------------------------------------------------------
// STEP 2: Create EWS threshold breach trigger
// -----------------------------------------------------------------------------
// This trigger fires when Actor nodes have EWS properties updated
// and breach defined thresholds

CALL apoc.trigger.add(
  'ewsThresholdBreachTrigger',
  '
  // Trigger fires on Actor property updates
  UNWIND $assignedNodeProperties AS nodeProps
  WITH nodeProps
  WHERE "Actor" IN labels(nodeProps.node)
    AND (
      nodeProps.node.ews_variance > 0.8 OR
      nodeProps.node.ews_autocorrelation > 0.9 OR
      nodeProps.node.ews_critical_distance < 0.2
    )

  // Determine severity
  WITH nodeProps.node AS actor,
       CASE
         WHEN nodeProps.node.ews_critical_distance < 0.1 THEN "CRITICAL"
         WHEN nodeProps.node.ews_critical_distance < 0.2 THEN "HIGH"
         WHEN nodeProps.node.ews_variance > 0.8 OR nodeProps.node.ews_autocorrelation > 0.9 THEN "MEDIUM"
         ELSE "LOW"
       END AS severity,
       CASE
         WHEN nodeProps.node.ews_critical_distance < 0.1 THEN "CRITICAL_SLOWING_DETECTED"
         WHEN nodeProps.node.ews_critical_distance < 0.2 THEN "APPROACHING_TRANSITION"
         WHEN nodeProps.node.ews_variance > 0.8 THEN "HIGH_VARIANCE_DETECTED"
         WHEN nodeProps.node.ews_autocorrelation > 0.9 THEN "HIGH_AUTOCORRELATION_DETECTED"
         ELSE "EWS_THRESHOLD_BREACH"
       END AS event_type

  // Create alert payload
  WITH actor, severity, event_type, {
    type: "ews_alert",
    timestamp: toString(datetime()),
    entity_id: actor.id,
    entity_type: "Actor",
    entity_name: actor.name,
    event: event_type,
    severity: severity,
    metrics: {
      variance: actor.ews_variance,
      autocorrelation: actor.ews_autocorrelation,
      critical_distance: actor.ews_critical_distance,
      last_updated: toString(actor.last_updated)
    },
    recommendation: CASE
      WHEN actor.ews_critical_distance < 0.1 THEN "Immediate intervention recommended"
      WHEN actor.ews_critical_distance < 0.2 THEN "Monitor closely, prepare intervention"
      WHEN actor.ews_variance > 0.8 THEN "System showing high volatility"
      WHEN actor.ews_autocorrelation > 0.9 THEN "System losing resilience"
      ELSE "Review EWS metrics"
    END
  } AS alert_payload

  // Publish to message queue (using APOC messaging)
  // Option 1: Use apoc.load.json to POST to WebSocket server
  CALL apoc.load.json(
    "http://localhost:3001/api/v1/ews/publish",
    null,
    {method: "POST", headers: {"Content-Type": "application/json"}, body: apoc.convert.toJson(alert_payload)}
  ) YIELD value

  // Option 2: Store in EWSAlert node for polling (fallback)
  CREATE (ea:EWSAlert {
    alert_id: apoc.create.uuid(),
    entity_id: alert_payload.entity_id,
    severity: alert_payload.severity,
    event_type: alert_payload.event,
    timestamp: datetime(),
    payload: apoc.convert.toJson(alert_payload),
    delivered: false
  })

  RETURN count(*) AS alerts_triggered
  ',
  {phase: 'after'}
);

// -----------------------------------------------------------------------------
// STEP 3: Alternative - Periodic scan trigger (if APOC trigger not available)
// -----------------------------------------------------------------------------
// This is a scheduled procedure that runs every N seconds to check for breaches

CALL apoc.periodic.repeat(
  'ewsPeriodicScan',
  '
  MATCH (a:Actor)
  WHERE a.ews_variance > 0.8
     OR a.ews_autocorrelation > 0.9
     OR a.ews_critical_distance < 0.2
  WITH a,
       CASE
         WHEN a.ews_critical_distance < 0.1 THEN "CRITICAL"
         WHEN a.ews_critical_distance < 0.2 THEN "HIGH"
         ELSE "MEDIUM"
       END as severity,
       CASE
         WHEN a.ews_critical_distance < 0.1 THEN "CRITICAL_SLOWING_DETECTED"
         WHEN a.ews_critical_distance < 0.2 THEN "APPROACHING_TRANSITION"
         WHEN a.ews_variance > 0.8 THEN "HIGH_VARIANCE_DETECTED"
         WHEN a.ews_autocorrelation > 0.9 THEN "HIGH_AUTOCORRELATION_DETECTED"
         ELSE "EWS_THRESHOLD_BREACH"
       END as event_type

  // Check if alert already sent recently (prevent spam)
  OPTIONAL MATCH (ea:EWSAlert)
  WHERE ea.entity_id = a.id
    AND ea.timestamp > datetime() - duration("PT5M")
  WITH a, severity, event_type, ea
  WHERE ea IS NULL  // Only create new alert if none in last 5 minutes

  // Create alert payload
  WITH a, severity, event_type, {
    type: "ews_alert",
    timestamp: toString(datetime()),
    entity_id: a.id,
    entity_type: "Actor",
    entity_name: a.name,
    event: event_type,
    severity: severity,
    metrics: {
      variance: a.ews_variance,
      autocorrelation: a.ews_autocorrelation,
      critical_distance: a.ews_critical_distance
    }
  } AS alert_payload

  // Store alert for delivery
  CREATE (ea:EWSAlert {
    alert_id: apoc.create.uuid(),
    entity_id: alert_payload.entity_id,
    severity: alert_payload.severity,
    event_type: alert_payload.event,
    timestamp: datetime(),
    payload: apoc.convert.toJson(alert_payload),
    delivered: false
  })

  RETURN count(*) AS new_alerts
  ',
  5  // Run every 5 seconds
);

// -----------------------------------------------------------------------------
// STEP 4: Management queries
// -----------------------------------------------------------------------------

// List all active triggers
CALL apoc.trigger.list() YIELD name, query, installed, paused
RETURN name, installed, paused, substring(query, 0, 100) + '...' AS query_preview;

// Pause trigger (for maintenance)
// CALL apoc.trigger.pause('ewsThresholdBreachTrigger');

// Resume trigger
// CALL apoc.trigger.resume('ewsThresholdBreachTrigger');

// Remove trigger
// CALL apoc.trigger.remove('ewsThresholdBreachTrigger');

// List periodic procedures
CALL apoc.periodic.list() YIELD name, delay, rate, done, cancelled
RETURN name, delay, rate, done, cancelled;

// Stop periodic scan
// CALL apoc.periodic.cancel('ewsPeriodicScan');

// -----------------------------------------------------------------------------
// STEP 5: Test trigger with sample data
// -----------------------------------------------------------------------------

// Create test Actor that breaches threshold
MERGE (a:Actor {id: 'TRIGGER-TEST-001'})
SET a.name = 'Trigger Test Actor',
    a.ews_variance = 0.95,  // Above 0.8 threshold
    a.ews_autocorrelation = 0.92,  // Above 0.9 threshold
    a.ews_critical_distance = 0.15,  // Below 0.2 threshold
    a.last_updated = datetime();

// Verify alert was created
MATCH (ea:EWSAlert)
WHERE ea.entity_id = 'TRIGGER-TEST-001'
RETURN ea.alert_id, ea.severity, ea.event_type, ea.timestamp, ea.delivered
ORDER BY ea.timestamp DESC
LIMIT 5;

// -----------------------------------------------------------------------------
// STEP 6: Alert delivery query (for WebSocket server polling)
// -----------------------------------------------------------------------------

// Get undelivered alerts
MATCH (ea:EWSAlert)
WHERE ea.delivered = false
  AND ea.timestamp > datetime() - duration('PT1H')  // Last hour only
WITH ea
ORDER BY ea.timestamp DESC
LIMIT 100
SET ea.delivered = true
RETURN ea.payload AS alert_json;

// Cleanup old delivered alerts (run periodically)
MATCH (ea:EWSAlert)
WHERE ea.delivered = true
  AND ea.timestamp < datetime() - duration('P7D')  // Older than 7 days
DETACH DELETE ea;

// =============================================================================
// END OF NEO4J TRIGGER CONFIGURATION
// =============================================================================
