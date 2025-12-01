// =============================================================================
// GAP-ML-005: WebSocket EWS Threshold Check Query
// =============================================================================
// File: src/ews-streaming/02_websocket_threshold_check.cypher
// Created: 2025-11-30
// Purpose: Query for real-time EWS threshold detection
// Database: bolt://aeon-neo4j-dev:7687
// =============================================================================

// -----------------------------------------------------------------------------
// MAIN THRESHOLD CHECK QUERY
// Purpose: Detect Actors breaching EWS thresholds for streaming alerts
// -----------------------------------------------------------------------------
MATCH (a:Actor)
WHERE a.ews_variance > 0.8
   OR a.ews_autocorrelation > 0.9
   OR a.ews_critical_distance < 0.2
WITH a,
     CASE
       WHEN a.ews_critical_distance < 0.1 THEN 'CRITICAL'
       WHEN a.ews_critical_distance < 0.2 THEN 'HIGH'
       WHEN a.ews_variance > 0.8 OR a.ews_autocorrelation > 0.9 THEN 'MEDIUM'
       ELSE 'LOW'
     END as severity,
     CASE
       WHEN a.ews_critical_distance < 0.1 THEN 'CRITICAL_SLOWING_DETECTED'
       WHEN a.ews_critical_distance < 0.2 THEN 'APPROACHING_TRANSITION'
       WHEN a.ews_variance > 0.8 THEN 'HIGH_VARIANCE_DETECTED'
       WHEN a.ews_autocorrelation > 0.9 THEN 'HIGH_AUTOCORRELATION_DETECTED'
       ELSE 'EWS_THRESHOLD_BREACH'
     END as event_type,
     CASE
       WHEN a.ews_critical_distance < 0.1 THEN 'Immediate intervention recommended'
       WHEN a.ews_critical_distance < 0.2 THEN 'Monitor closely, prepare intervention'
       WHEN a.ews_variance > 0.8 THEN 'System showing high volatility'
       WHEN a.ews_autocorrelation > 0.9 THEN 'System losing resilience'
       ELSE 'Review EWS metrics'
     END as recommendation

// Get related entities (optional - for context)
OPTIONAL MATCH (a)-[r]-(related:Actor)
WHERE related.ews_critical_distance IS NOT NULL
WITH a, severity, event_type, recommendation,
     collect(DISTINCT related.id)[0..5] as related_entities

// Return WebSocket event message format
RETURN {
  type: 'ews_alert',
  timestamp: toString(datetime()),
  entity_id: a.id,
  entity_type: 'Actor',
  entity_name: a.name,
  event: event_type,
  severity: severity,
  metrics: {
    variance: a.ews_variance,
    autocorrelation: a.ews_autocorrelation,
    critical_distance: a.ews_critical_distance,
    last_updated: toString(a.last_updated)
  },
  recommendation: recommendation,
  related_entities: related_entities
} AS alert
ORDER BY a.ews_critical_distance ASC, a.ews_variance DESC
LIMIT 100;

// =============================================================================
// FILTERED THRESHOLD CHECK (for subscription filters)
// =============================================================================

// Severity filter: CRITICAL only
MATCH (a:Actor)
WHERE a.ews_critical_distance < 0.1
WITH a, 'CRITICAL' as severity
RETURN {
  type: 'ews_alert',
  timestamp: toString(datetime()),
  entity_id: a.id,
  entity_type: 'Actor',
  event: 'CRITICAL_SLOWING_DETECTED',
  severity: severity,
  metrics: {
    variance: a.ews_variance,
    autocorrelation: a.ews_autocorrelation,
    critical_distance: a.ews_critical_distance
  },
  recommendation: 'Immediate intervention recommended'
} AS alert;

// Severity filter: HIGH or above
MATCH (a:Actor)
WHERE a.ews_critical_distance < 0.2
WITH a,
     CASE
       WHEN a.ews_critical_distance < 0.1 THEN 'CRITICAL'
       ELSE 'HIGH'
     END as severity
RETURN {
  type: 'ews_alert',
  timestamp: toString(datetime()),
  entity_id: a.id,
  entity_type: 'Actor',
  event: 'APPROACHING_TRANSITION',
  severity: severity,
  metrics: {
    variance: a.ews_variance,
    autocorrelation: a.ews_autocorrelation,
    critical_distance: a.ews_critical_distance
  }
} AS alert;

// =============================================================================
// SECTOR-SPECIFIC THRESHOLD CHECK
// =============================================================================

// Energy sector EWS alerts
MATCH (a:Actor)-[:OPERATES_IN]->(s:Sector {name: 'Energy'})
WHERE a.ews_variance > 0.8
   OR a.ews_autocorrelation > 0.9
   OR a.ews_critical_distance < 0.2
WITH a, s,
     CASE
       WHEN a.ews_critical_distance < 0.1 THEN 'CRITICAL'
       WHEN a.ews_critical_distance < 0.2 THEN 'HIGH'
       ELSE 'MEDIUM'
     END as severity
RETURN {
  type: 'ews_alert',
  timestamp: toString(datetime()),
  entity_id: a.id,
  entity_type: 'Actor',
  sector: s.name,
  event: 'SECTOR_EWS_BREACH',
  severity: severity,
  metrics: {
    variance: a.ews_variance,
    autocorrelation: a.ews_autocorrelation,
    critical_distance: a.ews_critical_distance
  }
} AS alert;

// =============================================================================
// TREND DETECTION QUERY (for delta alerts)
// =============================================================================

// Detect worsening EWS trends (requires temporal versioning)
MATCH (a:Actor)
WHERE a.ews_critical_distance IS NOT NULL
WITH a,
     a.ews_critical_distance as current_distance,
     a.ews_variance as current_variance,
     a.ews_autocorrelation as current_autocorr
// TODO: Compare with historical values when temporal versioning (GAP-ML-004) is implemented
// For now, alert on absolute thresholds
WHERE current_distance < 0.2
RETURN {
  type: 'ews_trend_alert',
  timestamp: toString(datetime()),
  entity_id: a.id,
  entity_type: 'Actor',
  event: 'EWS_WORSENING_TREND',
  severity: CASE
    WHEN current_distance < 0.1 THEN 'CRITICAL'
    ELSE 'HIGH'
  END,
  metrics: {
    variance: current_variance,
    autocorrelation: current_autocorr,
    critical_distance: current_distance
  },
  note: 'Trend detection requires GAP-ML-004 (Temporal Versioning)'
} AS alert;

// =============================================================================
// END OF THRESHOLD CHECK QUERIES
// =============================================================================
