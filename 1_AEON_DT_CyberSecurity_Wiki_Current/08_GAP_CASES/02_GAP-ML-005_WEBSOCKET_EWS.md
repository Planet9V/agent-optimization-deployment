# GAP-ML-005: WebSocket EWS Streaming

**File:** 02_GAP-ML-005_WEBSOCKET_EWS.md
**Gap ID:** GAP-ML-005
**Created:** 2025-11-30
**Priority:** CRITICAL
**Phase:** 1 - Foundation
**Effort:** L (4-6 weeks)
**Status:** NOT STARTED

---

## Problem Statement

**Current State:**
- EWS (Early Warning Signals) metrics calculated on-demand only
- Polling-based monitoring required
- No push notifications for critical events
- Latency too high for real-time crisis detection

**Desired State:**
- WebSocket streaming of EWS alerts
- Sub-second crisis detection capability
- Integration with incident response systems
- Push notifications for threshold breaches

---

## Technical Specification

### WebSocket Server Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EWS Streaming Service                     │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐         ┌──────────────┐                 │
│  │  Neo4j       │────────▶│  EWS Engine  │                 │
│  │  Triggers    │         │  (Calculator)│                 │
│  └──────────────┘         └──────┬───────┘                 │
│                                  │                          │
│                           ┌──────▼───────┐                 │
│                           │  WebSocket   │                 │
│                           │  Server      │                 │
│                           │  (Socket.io) │                 │
│                           └──────┬───────┘                 │
│                                  │                          │
│         ┌────────────────────────┼────────────────────┐    │
│         │                        │                    │    │
│  ┌──────▼───────┐   ┌──────▼───────┐   ┌──────▼───────┐  │
│  │ Frontend     │   │ PagerDuty   │   │ Slack       │  │
│  │ Dashboard    │   │ Integration │   │ Webhook     │  │
│  └──────────────┘   └──────────────┘   └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### WebSocket Protocol

```yaml
# Connection
ws://api.aeon-dt.com/v1/ews/stream

# Authentication
{
  "type": "auth",
  "token": "Bearer <jwt_token>"
}

# Subscription
{
  "type": "subscribe",
  "channels": ["ews:*", "cascade:*", "bifurcation:*"],
  "filters": {
    "severity": ["CRITICAL", "HIGH"],
    "sectors": ["energy", "water"]
  }
}

# Event Message (Server → Client)
{
  "type": "ews_alert",
  "timestamp": "2025-11-30T14:30:00Z",
  "entity_id": "ACTOR-001",
  "entity_type": "Actor",
  "event": "CRITICAL_SLOWING_DETECTED",
  "severity": "CRITICAL",
  "metrics": {
    "variance": 0.89,
    "autocorrelation": 0.94,
    "critical_distance": 0.12
  },
  "recommendation": "Immediate intervention recommended",
  "related_entities": ["ACTOR-002", "ASSET-015"]
}
```

### Neo4j Trigger Implementation

```cypher
// Trigger: Detect EWS threshold breach
// (Implemented as periodic procedure or CDC listener)

// EWS Threshold Check Query
MATCH (a:Actor)
WHERE a.ews_variance > 0.8
   OR a.ews_autocorrelation > 0.9
   OR a.ews_critical_distance < 0.2
WITH a,
     CASE
       WHEN a.ews_critical_distance < 0.1 THEN 'CRITICAL'
       WHEN a.ews_critical_distance < 0.2 THEN 'HIGH'
       ELSE 'MEDIUM'
     END as severity
RETURN a.id, severity, a.ews_variance, a.ews_autocorrelation, a.ews_critical_distance
```

---

## Implementation Steps

### Step 1: WebSocket Server (Week 1)
- [ ] Set up Socket.io server (Node.js/Express)
- [ ] Implement JWT authentication middleware
- [ ] Create subscription management system
- [ ] Build channel routing logic

### Step 2: EWS Engine (Week 2)
- [ ] Create EWS calculation service
- [ ] Implement threshold detection logic
- [ ] Build alert generation system
- [ ] Add severity classification

### Step 3: Neo4j Integration (Week 3)
- [ ] Create CDC (Change Data Capture) listener
- [ ] Implement periodic EWS scan procedure
- [ ] Build trigger for threshold breaches
- [ ] Connect Neo4j events to WebSocket server

### Step 4: Integrations (Week 4)
- [ ] PagerDuty webhook integration
- [ ] Slack notification channel
- [ ] Frontend dashboard subscription
- [ ] API documentation

---

## API Endpoints

```yaml
# REST Endpoints
GET /api/v1/ews/status
  Response: { streaming: true, connections: 45, alerts_24h: 12 }

POST /api/v1/ews/subscribe
  Request: { channels: [...], filters: {...} }
  Response: { subscription_id: "SUB-001", websocket_url: "ws://..." }

GET /api/v1/ews/history
  Query: severity, entity_id, from_date, to_date
  Response: { alerts: [...], pagination: {...} }

# WebSocket
ws://api.aeon-dt.com/v1/ews/stream
  - Auth message required first
  - Subscribe to channels
  - Receive real-time alerts
```

---

## Success Criteria

- [ ] WebSocket server operational and stable
- [ ] Alert latency <1 second from trigger to client
- [ ] 99.9% message delivery reliability
- [ ] Integration with PagerDuty functional
- [ ] Frontend dashboard receives real-time updates

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| High connection volume | Medium | Medium | Horizontal scaling, connection pooling |
| Message loss | High | Low | Implement acknowledgment, retry logic |
| Neo4j CDC overhead | Medium | Medium | Batch CDC reads, optimize queries |

---

## Dependencies

- GAP-ML-004 (Temporal Versioning) - for change detection
- Neo4j CDC or triggers operational
- WebSocket infrastructure

---

## Memory Keys

- `gap-ml-005-design`: Architecture decisions
- `gap-ml-005-progress`: Implementation progress
- `gap-ml-005-config`: Server configuration

---

## References

- API Spec: `mckenney-lacan-calculus-2025-11-28/neo4j-schema/04_MCKENNEY_LACAN_UNIFIED_API.yaml`
- EWS Theory: `mckenney-lacan-calculus-2025-11-28/Predictive_05_CRITICAL_SLOWING_DOWN_EWS.md`
